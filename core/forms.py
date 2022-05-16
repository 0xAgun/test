from django import forms
from .models import Userreports, Images
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Signupform(UserCreationForm):
    email = forms.EmailField()
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class Reportform(ModelForm):
    class Meta:
        model = Userreports
        fields = ['title', 'descrip', 'severity']
        # exclude = ['user', 'admin_approved']
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'descrip': forms.Textarea(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Report Title',
            'descrip': 'Description of the vuln'
        }

class ImageForm(ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
    class Meta:
        model = Images
        fields = ['image']