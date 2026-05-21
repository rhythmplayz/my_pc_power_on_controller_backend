from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ControlUser

class ControlUserAdmin(UserAdmin):
    # Display the verification status in the user list view
    list_display = ('username', 'email', 'is_verified', 'is_staff', 'is_superuser')
    
    # Allow quick toggle editing right from the list view
    list_editable = ('is_verified',)
    
    # Include the field when editing a specific user profile
    fieldsets = UserAdmin.fieldsets + (
        ('Verification Status', {'fields': ('is_verified',)}),
    )

admin.site.register(ControlUser, ControlUserAdmin)