from django import forms
from cities_light.models import Region, SubRegion
from . models import Mekan
class MekanForm(forms.ModelForm):
    sehir = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    ilce = forms.ModelChoiceField(queryset=SubRegion.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    aciklama = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Açıklama'}))

    class Meta:
        model = Mekan
        fields = ('adi', 'adres', 'sehir', 'ilce', 'aciklama', 'email', 'webadresi', 'telefon_numarasi')
        widgets = {
            'adi': forms.TextInput(attrs={'class': 'form-control'}),
            'adres': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_numarasi': forms.TextInput(attrs={'class': 'form-control'}),
            'webadresi': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'sehir' in self.data and self.data['sehir']:
            sehir_id = self.data['sehir']
            self.fields['ilce'].queryset = SubRegion.objects.filter(region_id=sehir_id).order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        sehir = cleaned_data.get('sehir')
        if sehir:
            ilce_queryset = SubRegion.objects.filter(region_id=sehir.id).order_by('name')
            self.fields['ilce'].queryset = ilce_queryset

        return cleaned_data
