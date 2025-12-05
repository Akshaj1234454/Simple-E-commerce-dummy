from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

class LogInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class reviewForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)])
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'comment-input',
            'rows': 4,
            'placeholder': 'Write your comment here...'
        }),
        required=False
    )