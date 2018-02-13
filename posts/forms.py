from django import forms
from .models import Post
import datetime

YEAR_CHOICES = tuple([2000+i for i in range(22)])

class PostForm(forms.ModelForm):

    title = forms.CharField(
        required=True, 
        label = "",
        widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'id':'id_title',
            'placeholder': "article title",
            'label':''
            }))


    timestamp = forms.DateField(
        label='Select Publish Date',
        initial = datetime.datetime.now(),
        widget=forms.SelectDateWidget(
            attrs={
                'class':'form-control',
                },
            years=YEAR_CHOICES)
    )

    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'id':'id_content',
                'rows':10,
                'placeholder': "article body",
                'label':''
                }))

    class Meta:
        model = Post
        fields = [
        'title',
        'content',
        'timestamp',
        ]