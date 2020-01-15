from django import forms
from .models import Analysis


class AnalysisTriggerForm(forms.Form):
    url = forms.URLField()

    def save(self):
        instance, created = Analysis.objects.get_or_create(url=self.cleaned_data['url'])
        return instance
