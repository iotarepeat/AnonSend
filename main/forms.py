from django import forms

from .models import UploadFiles


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFiles
        fields = ('file', 'expires_at', 'password')
        widgets = {
            'file': forms.ClearableFileInput(attrs={"multiple": True})
        }
