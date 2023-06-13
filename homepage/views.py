from datetime import datetime
import locale
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import calendar
from django.shortcuts import render, redirect
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

        
def home(request, year=None, month=None):
    # Varsayılan olarak geçerli yıl ve ayı ata
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().strftime('%B')

    data = create_calendar(year, month)

    # Şehirleri sorgula ve context'e ekle

    return render(request, 'home.html', data)
