from django.contrib import admin
from member.models import Member
from django.utils import timezone


class MemberAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "cpf", "is_admin", "created_at")
    list_filter = ("is_admin", "created_at")
    search_fields = ("email", "first_name", "last_name", "cpf")
    list_display_links = ("email", "first_name")

    exclude = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("email", "first_name", "last_name", "cpf", "contato", "is_admin", "last_login"),
        }),
        ("Autenticação", {
            "fields": ("password",),
            "classes": ("collapse",),
        }),
    )

    def save_model(self, request, obj, change):
        if not change or (obj.password and obj.password != obj._original_password):
            obj.set_password(obj.password)
        super().save_model(request, obj, change)


admin.site.register(Member, MemberAdmin)
