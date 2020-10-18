from django import forms


class UploadFileForm(forms.Form):
    file_input = forms.FileField(
        label="Choose CSV file(s) with plotting data: ")
