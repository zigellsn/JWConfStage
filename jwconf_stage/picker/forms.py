from django.forms import ModelForm, PasswordInput
from .models import Credential


class CredentialForm(ModelForm):
    class Meta:
        model = Credential
        fields = ['congregation', 'username', 'password', 'touch']
        widgets = { 
            'password': PasswordInput(),
        }