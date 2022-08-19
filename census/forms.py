from django import forms
from census.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', 'filetype', 'target', 'alpha')
