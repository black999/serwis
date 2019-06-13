from django.shortcuts import render, redirect, get_object_or_404
from .forms import KasaForm, PodatnikForm, PrzegladForm, PrzegladRokMiesiac
from .models import Model_kasy, Podatnik, Kasa, Przeglad
# from django.views.generic.list import ListView
import datetime


def home(request):
    kasy = Kasa.objects.filter(aktywna=True).order_by('nastepny_przeg')[:20]
    return render(request, 'kasy/przeglady_oczekujace.html', {'kasy': kasy})


# class ListaKas(ListView, pk):
#     template_name = 'kasy/kasa_lista.html'
#     queryset = Kasa.objects.all().select_related('podatnik')
#     model = Kasa
#     context_object_name = 'kasy'

def kasa_lista(request, typ):
    if typ == 'aktywne':
        kasy = Kasa.objects.filter(aktywna=True).select_related('podatnik')
    elif typ == 'nieaktywne':
        kasy = Kasa.objects.filter(aktywna=False).select_related('podatnik')
    elif typ == 'all':
        kasy = Kasa.objects.all().select_related('podatnik')
    return render(request, 'kasy/kasa_lista.html', {'kasy': kasy})


def kasa_szukaj(request):
    if request.method == 'POST':
        kasy = Kasa.objects.filter(
            nr_unikatowy__contains=request.POST['nr_unikatowy'])
        return render(request, 'kasy/kasa_lista.html', {'kasy': kasy})
    else:
        return redirect('home')


def kasa_dodaj(request, pk):
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            kasa = form.save(commit=False)
            kasa.model_kasy = Model_kasy.objects.get(
                pk=request.POST['model_kasy'])
            kasa.podatnik = Podatnik.objects.get(pk=pk)
            kasa.nastepny_przeglad(kasa.data_fisk)
            kasa.save()
            return redirect('podatnik_detale', pk=pk)
    else:
        form = KasaForm()
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def kasa_edycja(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    if request.method == 'POST':
        form = KasaForm(request.POST, instance=kasa)
        if form.is_valid():
            kasa = form.save(commit=False)
            ostatni_przeglad = Przeglad.objects.filter(
                kasa=pk).order_by('-data')
            if ostatni_przeglad.count() > 0:
                kasa.nastepny_przeglad(ostatni_przeglad[0].data)
            else:
                kasa.nastepny_przeglad(kasa.data_fisk)
            kasa.save()
            return redirect('kasa_detale', pk=pk)
    else:
        kasa.data_fisk = kasa.data_fisk.strftime('%Y-%m-%d')
        form = KasaForm(instance=kasa)
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def kasa_detale(request, pk):
    form = PrzegladForm()
    kasa = get_object_or_404(Kasa, pk=pk)
    przeglady = Przeglad.objects.filter(kasa=pk).order_by('-data')
    return render(request, 'kasy/kasa_detale.html',
                  {'kasa': kasa, 'form': form, 'przeglady': przeglady})


def kasa_przeglad(request, pk):
    if request.method == 'POST':
        form = PrzegladForm(request.POST)
        if form.is_valid():
            przeglad = form.save(commit=False)
            kasa = Kasa.objects.get(pk=pk)
            kasa.nastepny_przeglad(przeglad.data)
            kasa.save()
            przeglad.kasa = kasa
            przeglad.save()
            return redirect('kasa_detale', pk=pk)


def podatnik_dodaj(request):
    if request.method == 'POST':
        form = PodatnikForm(request.POST)
        if form.is_valid():
            podatnik = form.save(commit=False)
            podatnik.save()
            return redirect('podatnik_detale', pk=podatnik.pk)
    else:
        form = PodatnikForm()
    return render(request, 'kasy/podatnik_edycja.html', {'form': form})


def podatnik_lista(request):
    podatnicy = Podatnik.objects.all()
    return render(request, 'kasy/podatnik_lista.html',
                  {'podatnicy': podatnicy})


def podatnik_detale(request, pk):
    kasy = Kasa.objects.filter(podatnik=pk)
    podatnik = get_object_or_404(Podatnik, pk=pk)
    return render(request, 'kasy/podatnik_detale.html',
                  {'podatnik': podatnik, 'kasy': kasy})


def podatnik_edycja(request, pk):
    podatnik = get_object_or_404(Podatnik, pk=pk)
    if request.method == 'POST':
        form = PodatnikForm(request.POST, instance=podatnik)
        if form.is_valid():
            form.save()
            return redirect('podatnik_detale', pk=pk)
    else:
        form = PodatnikForm(instance=podatnik)
    return render(request, 'kasy/podatnik_edycja.html', {'form': form})


def przeglad_ostatnie(request):
    data = datetime.date.today()
    form = PrzegladRokMiesiac()
    przeglady = Przeglad.objects.filter(
        data__year=data.year, data__month=data.month)
    return render(request,
                  'kasy/przeglad_ostatnie.html',
                  {'przeglady': przeglady, 'form': form, 'data': data})


def przeglad_rok_miesiac(request, rok, mie):
    if request.method == 'POST':
        print(request.POST)
        return redirect('przeglad_rok_miesiac',
                        rok=request.POST['rok'], mie=request.POST['mie'])
    else:
        data = datetime.date.today()
        form = PrzegladRokMiesiac({'rok': rok, 'mie': mie})
        przeglady = Przeglad.objects.filter(data__year=rok, data__month=mie)
        return render(request,
                      'kasy/przeglad_ostatnie.html',
                      {'przeglady': przeglady, 'form': form, 'data': data})


def przeglad_faktura(request, pk):
    przeglad = get_object_or_404(Przeglad, pk=pk)
    przeglad.wystaw_fakture()
    przeglad.save()
    return redirect('przeglad_ostatnie')
