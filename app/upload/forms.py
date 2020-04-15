from django import forms

class UploadForm(forms.Form):
    dain = forms.BooleanField(initial=True, required=False)
    deoldify = forms.BooleanField(initial=True, required=False)
    esrgan = forms.BooleanField(initial=True, required=False)
    files = forms.FileField()