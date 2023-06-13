import locale
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import calendar
from datetime import date, datetime,timedelta

from django.urls import reverse

from .forms import MekanForm
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