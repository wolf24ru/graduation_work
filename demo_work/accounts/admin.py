from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'phone_number']
    fieldsets = (('Редактирование пользователя',
                  {'fields': ('username', 'email', 'phone_number',
                              'is_staff', 'is_active')
                   }
                  ),
                 )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'is_staff', 'is_active')
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
