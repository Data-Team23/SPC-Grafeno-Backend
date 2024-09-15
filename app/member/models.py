from djongo import models as mongo_models


class Member(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    username = mongo_models.CharField(max_length=150, unique=True)
    email = mongo_models.EmailField(max_length=254, unique=True)
    first_name = mongo_models.CharField(max_length=30, blank=True)
    last_name = mongo_models.CharField(max_length=30, blank=True)
    password = mongo_models.CharField(max_length=128)
    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        _use_db = "nonrel"
        ordering = ("-created_at", )

    def __str__(self):
        return self.username
