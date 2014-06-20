from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(label=u'Question', widget=forms.Textarea)


