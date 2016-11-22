from django import forms
from models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
    def clean(self):
        return self.cleaned_data
    def save(self):
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)
    def clean(self):
        pass
    def save(self):
        self.cleaned_data['question'] = Question.objects.get(id=self.cleaned_data['question'])
        return Answer.objects.create(**self.cleaned_data)
