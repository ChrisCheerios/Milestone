from django import forms

# The csv file upload form
class UploadFileForm(forms.Form):
    file = forms.FileField()
