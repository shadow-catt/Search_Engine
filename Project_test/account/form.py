# Programmer: Jack
# Student ID: 1930026143
# Date: 2020/1/24
# Requirements:

from django import forms

class LoginForm(forms.Form):
    acc_name = forms.CharField( max_length=20)
    acc_psd = forms.CharField( max_length=10, widget=forms.PasswordInput)
