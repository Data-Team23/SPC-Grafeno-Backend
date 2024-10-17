from djongo import models as mongo_models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class Member(mongo_models.Model):
    _id = mongo_models.ObjectIdField(primary_key=True)
    email = mongo_models.EmailField(max_length=254, unique=True)
    first_name = mongo_models.CharField(max_length=30, blank=True)
    last_name = mongo_models.CharField(max_length=30, blank=True)
    password = mongo_models.CharField(max_length=128)
    cpf = mongo_models.CharField(max_length=11, unique=True, default="")
    contato = mongo_models.CharField(max_length=15, blank=True, default="")
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)
    last_login = mongo_models.DateTimeField(null=True, blank=True)
    is_admin = mongo_models.BooleanField(default=False)

    class Meta:
        _use_db = "nonrel"
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
    
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)


class LGPDTerm(mongo_models.Model):
    user = mongo_models.ForeignKey(Member, on_delete=mongo_models.CASCADE)
    logs = mongo_models.TextField(blank=True, null=True)
    action_type = mongo_models.CharField(max_length=20, choices=[
        ("acceptance", "Acceptance"),
        ("update", "Update"),
        ("revoke", "Revoke"),
    ])
    acceptance_date = mongo_models.DateTimeField(auto_now_add=True)

    class Meta:
        _use_db = "nonrel"
