from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_management.models import User, LGPDGeneralTerm, LGPDTermItem, LGPDUserTermApproval


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Personal Info', {'fields': ('cpf', 'contato')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'cpf', 'contato', 'is_admin', 'is_staff', 'is_superuser')}
        ),
    )
    filter_horizontal = []
    list_filter = ['is_admin', 'is_staff', 'is_superuser']
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(LGPDGeneralTerm)
admin.site.register(LGPDTermItem)
admin.site.register(LGPDUserTermApproval)