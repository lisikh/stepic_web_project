from django import forms
from models import Question, Answer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login

class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
    #def __init__(self, *args, **kwargs):
        #self._user = args
        #super(AskForm, self).__init__(*args, **kwargs)
    def clean(self):
        return self.cleaned_data
    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    def clean(self):
        return self.cleaned_data
    def save(self):
        question = Question.objects.get(id=self.cleaned_data['question'])
        self.cleaned_data['question'] = question
        self.cleaned_data['author'] = self._user
        answer = Answer.objects.create(**self.cleaned_data)
        question.rating += 1
        question.save()
        return answer


class NewUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    #last_login = forms.DateTimeField(widget=forms.HiddenInput)

    def clean(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except:
            return self.cleaned_data
        raise forms.ValidationError(u'User exists')

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        password = self.cleaned_data['password']
        authenticate(username=user, password=password)
        self.cleaned_data['user'] = user



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            self.cleaned_data['user'] = user
            return self.cleaned_data
        else:
            raise forms.ValidationError('User or password not correct')