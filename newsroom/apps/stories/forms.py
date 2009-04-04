from django import forms
from newsroom.models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('author','created','modified',)
        



