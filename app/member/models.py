from djongo import models as mongo_models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class Member(mongo_models.Model):
    _id = mongo_models.ObjectIdField(primary_key=True)
    username = mongo_models.CharField(max_length=150, unique=True)
    email = mongo_models.EmailField(max_length=254, unique=True)
    first_name = mongo_models.CharField(max_length=30, blank=True)
    last_name = mongo_models.CharField(max_length=30, blank=True)
    password = mongo_models.CharField(max_length=128)
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)
    last_login = mongo_models.DateTimeField(null=True, blank=True)

    class Meta:
        _use_db = "nonrel"
        ordering = ("-created_at", )

    def __str__(self):
        return self.username
    
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)
