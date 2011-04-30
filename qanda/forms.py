from django import forms
from qanda.models import Category

class QuestionForm(forms.Form):
    title = forms.CharField()
    question = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField()
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget=forms.CheckboxSelectMultiple)

class AnswerForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)