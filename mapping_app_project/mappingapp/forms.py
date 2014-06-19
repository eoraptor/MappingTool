from django import forms
#from multiuploader.forms import MultiuploaderField

class UploadFileForm(forms.Form):
    title = forms.CharField(label=u'Question', widget=forms.Textarea)
    #uploadedFiles = MultiuploaderField(required=False)

