from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone")
    
    def clean_username(self):
        """Converte username para minúscula (case-insensitive)"""
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone")
    
    def clean_username(self):
        """Converte username para minúscula (case-insensitive)"""
        username = self.cleaned_data.get('username')
        if username:
            return username.lower()
        return username