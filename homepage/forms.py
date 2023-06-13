from django import forms
from cities_light.models import Region, SubRegion
from .models import Profile
from homepage.models import Mekan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Parola doğrulama işlemlerini burada gerçekleştirin
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parolalar eşleşmiyor.")
        
        # Diğer parola doğrulama kurallarını burada kontrol edin
        # Örneğin, parolanın en az 8 karakter içermesi gerektiğini kontrol edebilirsiniz

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta zaten kullanılıyor.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    profile_img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Profile
        fields = ['ad', 'soyad', 'telefon', 'email', 'username', 'profile_img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.user.email
        self.fields['email'].label = 'E-Posta Adresi'
        self.fields['username'].initial = self.instance.user.username
        self.fields['username'].label = 'Kullanıcı Adı'
        self.fields['new_password1'].label = 'Yeni Şifre'
        self.fields['new_password2'].label = 'Tekrar Şifre'

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and not new_password2:
            raise forms.ValidationError("Lütfen yeni şifreyi tekrar girin.")

        if new_password1 != new_password2:
            raise forms.ValidationError("Yeni şifreler eşleşmiyor.")

        return cleaned_data

    def save(self, commit=True):
        user = self.instance.user
        new_password = self.cleaned_data.get('new_password1')

        if new_password:
            user.set_password(new_password)
            user.save()

        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        # Profil resmi dosyasını kaydetme işlemi
        profile_img = self.cleaned_data.get('profile_img')
        if profile_img:
            profile.profile_img = profile_img
            profile.save()

        return profile
