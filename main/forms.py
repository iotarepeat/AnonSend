from django import forms
from django.core.exceptions import ValidationError

from main.helper import verifyPassword
from .models import UploadFile, ReportLink


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file', 'expires_at', 'max_downloads', 'password')
        widgets = {
            'file': forms.ClearableFileInput(attrs={"multiple": True}),
            'password': forms.PasswordInput(),
        }


class ReportFileForm(forms.ModelForm):
    class Meta:
        model = ReportLink
        fields = '__all__'
        exclude = ['upload_file']
        widgets = {
            'reason': forms.RadioSelect(),
            'description': forms.Textarea(attrs={"rows": 5, "cols": ""})
        }


class PasswordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self.expected_password = kwargs.pop("expected_password")
        except KeyError:
            self.expected_password = None
        super(PasswordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UploadFile
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        if not verifyPassword(self.cleaned_data['password'], self.expected_password):
            self.add_error("password", ValidationError(message="Invalid Password"))
            raise ValidationError(message="Invalid Password")
        return self.cleaned_data
