from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cities_light.models import SubRegion, Region
class Mekan(models.Model):
    adi = models.CharField('Mekan Adı', max_length=20)
    adres = models.CharField(max_length=300)
    telefon_numarasi = models.CharField('Telefon', max_length=11)
    webadresi = models.URLField('Website Adresi')
    email = models.EmailField('Email Adresi')
    sehir = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='sehir')
    ilce = models.ForeignKey(SubRegion, on_delete=models.SET_NULL, null=True, blank=True)
    aciklama = models.TextField('Mekan Açıklaması', null=True, blank=True)
    olusturan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    onayli = models.BooleanField('Onaylı', default=False)
    onay_tarihi = models.DateTimeField('Onay Tarihi', null=True, blank=True)
    silindi = models.BooleanField('Silindi',default='False')
    acik = models.BooleanField('Etkinliğe Açık',default=False)
    olumlu_oy = models.PositiveIntegerField(default=0)
    olumlu_oy_kullananlar = models.ManyToManyField(User, related_name='olumlu_oylar',null=True,blank=True)
    olumsuz_oy = models.PositiveIntegerField(default=0)
    olumsuz_oy_kullananlar = models.ManyToManyField(User, related_name='olumsuz_oylar',null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.onayli and not self.onay_tarihi:
            self.onay_tarihi = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.adi