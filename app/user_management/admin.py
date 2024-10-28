from django.contrib import admin
from user_management.models import User, LGPDGeneralTerm, LGPDTermItem, LGPDUserTermApproval


class UserAdmin(admin.ModelAdmin):
    readonly_fields  = ('id', 'email', 'first_name', 'last_name', 'created_at', 'is_admin')

admin.site.register(User, UserAdmin)
admin.site.register(LGPDGeneralTerm)
admin.site.register(LGPDTermItem)
admin.site.register(LGPDUserTermApproval)
