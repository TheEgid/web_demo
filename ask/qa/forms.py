from django import forms
from .models import Question, Answer


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
