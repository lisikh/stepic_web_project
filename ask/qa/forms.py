from django import forms
from models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
    def clean(self):
        pass
    def save(self):
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question_id = forms.IntegerField(widget=forms.HiddenInput)
    def clean(self):
        pass
    def save(self):
        print(self.cleaned_data)
        return Answer.objects.create(**self.cleaned_data)
