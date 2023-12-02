from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'grade')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'grade'),
        }),
    )

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'grade']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'grade']
    list_filter = ['is_active', 'grade']


# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
# rahhali -> Csd_@_2023
# don -> 1997

admin.site.register(Stagiaire)
admin.site.register(Consultation)
admin.site.register(Permission)
admin.site.register(Renseignement)
admin.site.register(Reservation)
admin.site.register(Groupe)

