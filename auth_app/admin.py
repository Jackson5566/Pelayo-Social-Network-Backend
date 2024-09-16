from django.contrib import admin
from .models import User

# Register your models here.

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data['password']:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)
