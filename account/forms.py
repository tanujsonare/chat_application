from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            })
        }


class AddAdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'password',)
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            })
        }


class AddUserForm(forms.ModelForm):
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full py-2 my-3 px-6 rounded-xl border'}))
    class Meta:
        model = User
        fields = ('email', 'name', 'password')
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full py-2 my-3 px-6 rounded-xl border'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        retype_password = cleaned_data.get('retype_password')

        if password and retype_password and password != retype_password:
            self.add_error('retype_password', "Passwords does not match !!")

        return cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role',)
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-4 my-3 px-6 rounded-xl border'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full py-4 my-3 px-6 rounded-xl border'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full py-4 my-3 px-6 rounded-xl border'
            })
        }