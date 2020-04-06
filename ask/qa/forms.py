from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


class AskForm(forms.Form):
    title = forms.CharField(max_length=30, widget=forms.Textarea)
    text = forms.CharField(max_length=255, widget=forms.Textarea)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self, user):
        question = Question(**self.cleaned_data)
        question.author = user
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()
    question_id = forms.IntegerField()

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def save(self, author):
        del self.cleaned_data['question']
        answer = Answer(**self.cleaned_data)
        answer.author = author
        answer.save()
        return answer


# class RegistForm(forms.Form):
#     pass
#
#
# class LoginForm(forms.Form):
#     username = forms.CharField()
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#
#     def clean(self):
#         cleaned_data = super(LoginForm, self).clean()
#         # print 'create',cleaned_data
#         password = cleaned_data['password']
#         # password1 = cleaned_data['password1']
#         try:
#             user = User.objects.get(username=cleaned_data['username'])
#             return None
#         except ObjectDoesNotExist:
#             pass
#
#         try:
#             user = User.objects.get(email=cleaned_data['email'])
#             return None
#         except ObjectDoesNotExist:
#             pass
#
#         return cleaned_data
#         # if password and password1 and password == password1:
#         #     return cleaned_data
#         # else:
#         #     return None
#
#     def save(self):
#         username = self.cleaned_data["username"]
#         email = self.cleaned_data["email"]
#         password = self.cleaned_data["password"]
#         user = User.objects.create_user(username, email, password)
#         user.save()
#         user = authenticate(username=username, password=password)
#         return user

#
# class LoginForm(forms.Form):
#     username = forms.CharField(
#         required=True,
#         label=r'Username',
#         error_messages={'required': 'Please enter your username'},
#         widget=forms.TextInput(attrs={'placeholder': r'username'}))
#     password = forms.CharField(
#         required=True,
#         label=r'Password',
#         error_messages={'required': 'Please enter your password'},
#         widget=forms.PasswordInput(attrs={'placeholder': r'Password'}))
#
#     def clean(self):
#         if not self.is_valid():
#             raise forms.ValidationError(u'Both email and password are required')
#         cleaned_data = super(LoginForm, self).clean()
#         return cleaned_data
#
#
# class RegistForm(forms.Form):
#     username = forms.CharField(
#         required=True,
#         label=r'Username',
#         error_messages={'required': 'Required fields'},
#         widget=forms.TextInput(attrs={'placeholder': r'Username'}))
#     email = forms.EmailField(
#         required=True,
#         label=r'Email address',
#         error_messages={'required': 'Mailbox must be legal'},
#         widget=forms.EmailInput(attrs={'placeholder': r'Email address'}))
#     password = forms.CharField(
#         required=True,
#         label=r'Password',
#         error_messages={'required': 'Please enter your password'},
#         widget=forms.PasswordInput(attrs={'placeholder': r'Password'}))
#     re_password = forms.CharField(
#         required=True,
#         label=r'Repeat password',
#         error_messages={'required': 'Please enter the password again'},
#         widget=forms.PasswordInput(attrs={'placeholder': r'Repeat password'}))
#
#     def clean(self):
#         if not self.is_valid():
#             raise forms.ValidationError(r'Incomplete information')
#         cleaned_data = super(RegistForm, self).clean()
#         return cleaned_data


#forms
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',  'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']