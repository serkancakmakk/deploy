# Generated by Django 4.1.7 on 2023-06-13 11:23

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import homepage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=120, verbose_name='Etkinlik Adı')),
                ('baslik', models.CharField(blank=True, max_length=50, null=True, verbose_name='Baslik')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('saat', models.TimeField(verbose_name='Saat')),
                ('gün', models.DateTimeField(verbose_name='Etkinlik Günü')),
                ('katilimci_kontrol', models.BooleanField(default=False)),
                ('kontenjan', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('açiklama', ckeditor.fields.RichTextField()),
                ('silindi', models.BooleanField(default=False)),
                ('katilimcilar', models.ManyToManyField(blank=True, related_name='katildigi_etkinlikler', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=20)),
                ('soyad', models.CharField(max_length=20)),
                ('profile_img', models.ImageField(upload_to=homepage.models.user_directory_path)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefon', models.CharField(blank=True, max_length=11, null=True)),
                ('kayit_tarihi', models.DateTimeField(auto_now_add=True)),
                ('katildigi_etkinlikler', models.ManyToManyField(blank=True, related_name='katilimcilar_profil', to='homepage.event')),
                ('olusturdugu_etkinlikler', models.ManyToManyField(blank=True, related_name='olusturan_profil', to='homepage.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mekan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi', models.CharField(max_length=20, verbose_name='Mekan Adı')),
                ('adres', models.CharField(max_length=300)),
                ('telefon_numarasi', models.CharField(max_length=11, verbose_name='Telefon')),
                ('webadresi', models.URLField(verbose_name='Website Adresi')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Adresi')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Mekan Açıklaması')),
                ('onayli', models.BooleanField(default=False, verbose_name='Onaylı')),
                ('onay_tarihi', models.DateTimeField(blank=True, null=True, verbose_name='Onay Tarihi')),
                ('silindi', models.BooleanField(default='False', verbose_name='Silindi')),
                ('acik', models.BooleanField(default=False, verbose_name='Etkinliğe Açık')),
                ('olumlu_oy', models.PositiveIntegerField(default=0)),
                ('olumsuz_oy', models.PositiveIntegerField(default=0)),
                ('ilce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.subregion')),
                ('olumlu_oy_kullananlar', models.ManyToManyField(blank=True, null=True, related_name='olumlu_oylar', to=settings.AUTH_USER_MODEL)),
                ('olumsuz_oy_kullananlar', models.ManyToManyField(blank=True, null=True, related_name='olumsuz_oylar', to=settings.AUTH_USER_MODEL)),
                ('olusturan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sehir', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sehir', to='cities_light.region')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='mekan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etkinlikler', to='homepage.mekan'),
        ),
        migrations.AddField(
            model_name='event',
            name='yönetici',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='yönetici_event_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
