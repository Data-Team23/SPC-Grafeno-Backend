from django.contrib import admin
from member import models

admin.site.register(models.Member)
admin.site.register(models.LGPDTerm)
