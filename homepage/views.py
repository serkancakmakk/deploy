import locale
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
import calendar
from datetime import datetime
from cities_light.models import SubRegion

from django.shortcuts import redirect, render
import locale
import calendar
from datetime import datetime
from django.urls import reverse

from .models import Profile
from .forms import MekanForm, ProfileUpdateForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from cities_light.models import SubRegion
from .forms import MekanForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from django.urls import reverse

from .forms import MekanForm
def get_ilceler(request, sehir_id):
    ilceler = SubRegion.objects.filter(region_id=sehir_id).values('id', 'name')
    return JsonResponse(list(ilceler), safe=False)
def home(request, year=None, month=None):
    # Varsayılan olarak geçerli yıl ve ayı ata
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')

    data = create_calendar(year, month)

    return render(request, 'home.html', data)

def create_calendar(year, month):#iki viewsda da aynısnı yapmamak için ayrı bir fonksiyon tanımladım
    # Türkçe ay adını ayarlama
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
    month = month.capitalize()
    # Ayları isimden sayıya dönüştür
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Takvimi oluştur
    cal = calendar.HTMLCalendar().formatmonth(year, month_number)

    # Şimdiki yılı ve saati getir
    now = datetime.now()
    current_year = now.year
    time = now.strftime('%I:%M:%S')
    day = now.day

    # Bir sonraki ayın adını ve yılını hesapla
    if month_number == 12:
        next_month_number = 1
        next_year = year + 1
    else:
        next_month_number = month_number + 1
        next_year = year

    current_month = calendar.month_name[now.month]
    next_month = calendar.month_name[next_month_number]

    return {

        "year": year,
        "day": day,
        "month": month,
        "current_month": current_month,
        "month_number": month_number,
        "cal": cal,
        "now": now,
        "current_year": current_year,
        "time": time,
        "next_month": next_month.lower(),
        "next_year": next_year,
    }
def mekanekle(request, year=None, month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')
    
    submitted = False
    
    if request.method == "POST":
        form = MekanForm(request.POST)
        if form.is_valid():
            mekan = form.save(commit=False)
            if request.user.is_authenticated:
                mekan.olusturan = request.user
            mekan.save()
            submitted = True
            return HttpResponseRedirect(reverse('mekanekle') + '?submitted=True')
    else:
        form = MekanForm()
    
    if 'submitted' in request.GET:
        submitted = True
    
    data = create_calendar(year, month)
    return render(request, 'yer_ekle.html', {'form': form, **data, 'submitted': submitted})
from django.contrib import messages

def login_view(request,year=None,month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')
        data = create_calendar(year, month)
    user = request.user
    if user.is_authenticated: #Kullanıcı giriş yapmış ve tekrar login olmaya çalışırsa logout edilir.
        
        return redirect('logout')
    else:
        if request.method == 'POST':
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user is not None:
                    if hasattr(user, 'profile'):
                        return redirect('home')
                    else:
                        return redirect('update_profile')
                else:
                    messages.error(request, 'Kullanıcı adı veya şifre yanlış.')

    
    return render(request, 'login.html', data)
def my_profile(request, year=None, month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')
    data = create_calendar(year, month)
    user = request.user
    katildigi_etkinlikler = user.profile.katildigi_etkinlikler.all()
    katildigi_etkinlik_sayisi = katildigi_etkinlikler.count()
    olusturdugu_etkinlikler = user.profile.olusturdugu_etkinlikler.all()
    olusturdugu_etkinlik_sayisi = olusturdugu_etkinlikler.count()
    son_etkinlikler = olusturdugu_etkinlikler.order_by('-id')
    son_etkinliklerim = son_etkinlikler[:2]
    context = {
        'user': user,
        'katildigi_etkinlikler': katildigi_etkinlikler,
        'katildigi_etkinlik_sayisi': katildigi_etkinlik_sayisi,
        'olusturdugu_etkinlikler': olusturdugu_etkinlikler,
        'olusturdugu_etkinlik_sayisi': olusturdugu_etkinlik_sayisi,
        'son_etkinliklerim': son_etkinliklerim
    }
    context.update(data)  # data sözlüğünü context sözlüğüne güncelle
    return render(request, 'profile/my_profile.html', context)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
def update_profile(request, year=None, month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')

    data = create_calendar(year, month)

    try:
        event_user = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        event_user = None

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=event_user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if not profile.profile_img:  # Eğer resim alanı boş bırakıldıysa
                profile.profile_img = event_user.profile_img  # Mevcut profil resmini koru
            user = request.user  # user değişkenini tanımla
            profile.user = user
            profile.save()

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)

            return redirect('my_profile')
    else:
        form = ProfileUpdateForm(instance=event_user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile/profili_güncelle.html', {'form': form, 'password_form': password_form, **data})
from django.contrib.auth import logout
def register(request,year=None,month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')

    data = create_calendar(year, month)
    user = request.user
    if user.is_authenticated:
        logout(request)
        return redirect('register')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # Kullanıcı başarıyla kaydedildikten sonra giriş sayfasına yönlendirilebilirsiniz
        else:
            form = RegistrationForm()
        return render(request, 'register.html', {'form': form, **data})
