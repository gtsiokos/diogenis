from django import forms

class StudentSignupForm(forms.Form):
    dionysos_username = forms.CharField(max_length = 30, label = 'onoma xristi sto dionyso')
    dionysos_password = forms.CharField(max_length = 30, label = 'password xristi', widget = forms.PasswordInput())

