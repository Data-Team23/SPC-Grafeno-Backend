import uuid
from datetime import timezone
from django.db import models
from cryptography.fernet import Fernet
from mongo_client import encrypt_db, logs_db


def generate_encryption_key():
    return Fernet.generate_key()


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    cpf = models.CharField(max_length=255, unique=True)
    contato = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.encryption_key = generate_encryption_key()
        
        fernet = Fernet(self.encryption_key)

        self.email = fernet.encrypt(self.email.encode()).decode()
        self.first_name = fernet.encrypt(self.first_name.encode()).decode()
        self.last_name = fernet.encrypt(self.last_name.encode()).decode()
        self.password = fernet.encrypt(self.password.encode()).decode()
        self.cpf = fernet.encrypt(self.cpf.encode()).decode()
        self.contato = fernet.encrypt(self.contato.encode()).decode()

        super().save(*args, **kwargs)

        encrypt_db.userEncrypt.update_one(
            {'user_id': str(self.id)},
            {'$set': {'key': self.encryption_key.decode()}},
            upsert=True
        )


class LGPDGeneralTerm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    term_type = models.ForeignKey('LGPDTermItem', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class LGPDTermItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_mandatory = models.BooleanField(default=False)


class LGPDUserTermApproval(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    general_term = models.ForeignKey(LGPDGeneralTerm, on_delete=models.CASCADE)
    approved = models.BooleanField()
    approval_date = models.DateTimeField(auto_now_add=True)
    logs = models.TextField()


class ActionLog:
    def __init__(self, user_id, action_type, logs):
        self.collection = logs_db.ActionLog
        self.user_id = user_id
        self.action_type = action_type
        self.logs = logs

    def save(self):
        action_log = {
            'id': str(uuid.uuid4()),
            'user_id': self.user_id,
            'action_type': self.action_type,
            'action_date': timezone.now(),
            'logs': self.logs
        }
        self.collection.insert_one(action_log)
