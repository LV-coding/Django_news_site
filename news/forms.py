from dataclasses import fields
from django import forms
from .models import Link


"""
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('link_title', 'link_url', ) 
        labels = {
            'link_url': ('Адреса URL'),
            'link_title': ('Назва посилання')
        }
        widgets = {'link_title': forms.TextInput(attrs={
                'class': "field-link"
                }),
                'link_url': forms.TextInput(attrs={
                'class': "field-link"
                })
        }
"""