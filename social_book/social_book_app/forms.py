from django import forms
from .models import CustomUser,UploadedFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email','address',
                  'public_visiblity'
                  )


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('title', 'description', 'visibility', 'cost', 'year_published', 'file')