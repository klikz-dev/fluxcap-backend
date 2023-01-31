from settings.models import Site
from django import forms


class SiteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Site
        fields = '__all__'
