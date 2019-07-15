from django import forms

from .models import uploadModel


class uploadFileForm(forms.ModelForm):
    class Meta:
        model = uploadModel
        fields = ('file',)
