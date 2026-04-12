from django import forms
from unfold.forms import AdminPasswordChangeForm as BaseAdminPasswordChangeForm
from unfold.forms import UserChangeForm as BaseUserChangeForm
from unfold.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "first_name", "last_name")


class AccountSignupForm(forms.Form):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save(update_fields=["first_name", "last_name"])


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class AdminPasswordChangeForm(BaseAdminPasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"