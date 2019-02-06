from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import GuestEmail
from .forms import UserAdminChangeForm, UserAdminCreationForm

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm # update
    add_form = UserAdminCreationForm # create

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        # ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff', 'active')}),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email','full_name')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin.
admin.site.unregister(Group)



class GuestEmailAdmin(admin.ModelAdmin):
    search_fields=['email']
    class Meta:
        model = User
admin.site.register(GuestEmail, GuestEmailAdmin)