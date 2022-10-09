from django import forms
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .. import models

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = models.User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = '__all__'

class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(attrs={'autocomplete': 'on'}))


class PhysicalAppForm(forms.ModelForm):
    class Meta:
        model = models.PhysicalApplication
        exclude = ["status", "date"]
        
class OrgAppForm(forms.ModelForm):
    class Meta:
        model = models.OrgApplication
        exclude = ["status", "date"]