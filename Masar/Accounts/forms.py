from django.contrib.auth.forms import UserCreationForm

from .models import User


class DispatcherCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.DISPATCHER  # the form can only ever create dispatchers
        if commit:
            user.save()
        return user


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "role")