from django import forms

from .models import uploadModel


class uploadFileForm(forms.ModelForm):
    class Meta:
        model = uploadModel
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={"multiple": True})
        }
