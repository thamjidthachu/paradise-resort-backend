from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    model = User
    list_display = ('email', 'is_active',)
    list_filter = ('is_active',)
    filter_horizontal = ('user_roles',)

    admin_for_add_users = 'admin@view.com'

    def get_queryset(self, request):
        user_perms = ['registration.add_user', 'registration.change_user',
                      'registration.delete_user', 'registration.view_user']

        # if request.user.user_permissions.all().count() == 4 and request.user.has_perms(user_perms):
        #     self.admin_for_add_users = request.user.email
        #     if request.user.email == self.admin_for_add_users:
        #         return User.objects.exclude(is_staff=True)

        return User.objects.all()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.email if request.user.email == self.admin_for_add_users else None

        if is_superuser:
            form.base_fields['groups'].widget = forms.HiddenInput()


        return form

    fieldsets = (
        (None, {'fields': (
            'email', 'password', "userName", "role", "gender", 'Phone', 'full_name', 'signature', 'user_roles',
            'user_major')}),
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ('User Info', {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password', 'userName', "role", "gender", 'Phone', 'user_major',)}
         ),
        ('User Permissions', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', 'is_active')}
         ),
        ('Signature', {
            'classes': ('wide',),
            'fields': ('signature',)
        })
    )

    search_fields = ('email',)
    ordering = ('email',)


# Re-register UserAdmin
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
