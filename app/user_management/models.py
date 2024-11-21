from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from cryptography.fernet import Fernet
from mongo_client import encrypt_db, logs_db
from django.utils import timezone

import base64
import uuid


class ActionLog:
    def __init__(self, user_id, action_type, logs):
        self.user_id = user_id
        self.action_type = action_type
        self.logs = logs
        self.collection = self.get_collection()

    def get_collection(self):
        collections = sorted(logs_db.list_collection_names(), reverse=True)
        last_collection_name = next((c for c in collections if c.startswith("ActionLog_")), None)

        if not last_collection_name or logs_db[last_collection_name].count_documents({}) >= 10000:
            new_collection_name = f"ActionLog_{len(collections) + 1}"
            return logs_db[new_collection_name]
        else:
            return logs_db[last_collection_name]

    def save(self):
        action_log = {
            'id': str(uuid.uuid4()),
            'user_id': self.user_id,
            'action_type': self.action_type,
            'action_date': timezone.now(),
            'logs': self.logs
        }
        self.collection.insert_one(action_log)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um email")
        if not username:
            raise ValueError("O usuário deve ter um nome de usuário")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    cpf = models.CharField(max_length=255, unique=True)
    contato = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    # Django Admin
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        is_update = self.__class__.objects.filter(pk=self.pk).exists()
        
        if is_update and 'update_fields' not in kwargs:
            kwargs['update_fields'] = ['updated_at']

        encryption_key = Fernet.generate_key()
        encryption_key_base64 = base64.urlsafe_b64encode(encryption_key).decode()
        fernet = Fernet(encryption_key)
        
        self.email = fernet.encrypt(self.email.encode())
        self.first_name = fernet.encrypt(self.first_name.encode())
        self.last_name = fernet.encrypt(self.last_name.encode())
        self.cpf = fernet.encrypt(self.cpf.encode())
        self.contato = fernet.encrypt(self.contato.encode())
        super().save(*args, **kwargs)

        encrypt_db.userEncrypt.update_one(
            {'user_id': str(self.id)},
            {'$set': {'key': encryption_key_base64}},
            upsert=True
        )

        action_type = "update" if is_update else "register"
        log_message = "User data updated" if is_update else "User register"
        ActionLog(user_id=str(self.id), action_type=action_type, logs=log_message).save()

    def login(self):
        ActionLog(user_id=str(self.id), action_type="login", logs="User logged in").save()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def decrypt_data(self):
        try:
            user_encryption_data = encrypt_db.userEncrypt.find_one({'user_id': str(self.id)})
            if not user_encryption_data:
                return None
            
            encryption_key = user_encryption_data['key']
            encryption_key = base64.urlsafe_b64decode(encryption_key)
            fernet = Fernet(encryption_key)

            decrypted_data = {
                'email': self._decrypt_field(fernet, self.email),
                'username': self.username,
                'first_name': self._decrypt_field(fernet, self.first_name),
                'last_name': self._decrypt_field(fernet, self.last_name),
                'cpf': self._decrypt_field(fernet, self.cpf),
                'contato': self._decrypt_field(fernet, self.contato),
            }
            return decrypted_data
        except Exception as e:
            return {"detail": str(e)}

    def _decrypt_field(self, fernet, encrypted_message):
        if encrypted_message.startswith("b'") and encrypted_message.endswith("'"):
            encrypted_message = encrypted_message[2:-1]
        decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
        return decrypted_message


class LGPDTermItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class LGPDGeneralTerm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    term_itens = models.ManyToManyField(LGPDTermItem, blank=True, related_name="general_terms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LGPDUserTermApproval(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    general_term = models.ForeignKey('LGPDGeneralTerm', on_delete=models.CASCADE)
    items_term = models.ForeignKey('LGPDTermItem', on_delete=models.CASCADE, null=True)
    approval_date = models.DateTimeField(auto_now_add=True)
    logs = models.TextField()

    def __str__(self):
        return f"Aprovação do {self.user.username}"