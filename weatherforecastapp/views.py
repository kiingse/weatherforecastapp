from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages


from .forms import CreateUserForm, FindCityForm
from .models import *
from .decorators import unauthenticated_user
from .api import kelvin_to_celsius_conv, coordinates_fun, get_weather_data

def HomePage(request):

    if request.user.is_authenticated:
        user_cities = Cities.objects.filter(owner_id = request.user)
        no_of_cities = len(user_cities)

        context = {
            'user_cities':user_cities,
            'no_of_cities':no_of_cities,
                }
        
    else:
        context = {}

    return render(request, 'index.html', context)


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Pomyślnie zarejestrowano. Możesz się teraz zalogować.')
            return redirect('home_page')
        else:
            try:
                user_in_db = User.objects.get(username = form.data['username'])

                if user_in_db is not NULL:
                    messages.info(request, 'Użytkownik o takiej nazwie już istnieje. Wybierz inną nazwę.')
            except:
                messages.error(request, 'Coś poszło nie tak, spróbuj ponownie.')
                return redirect('register')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_auth(request, user)
            messages.success(request, 'Zalogowano pomyślnie.')
            return redirect('home_page')
        else:
            messages.info(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')
            return redirect('login')

    context = {}
    return render(request, 'accounts/login.html', context)


def logout(request):
    logout_auth(request)
    return redirect('home_page')


@login_required
def AddCity(request):
    
    form = FindCityForm()
    
    if request.method == 'POST':
        form = FindCityForm(request.POST)

        if form.is_valid():
            city_in_db = Cities.objects.filter(city = form.cleaned_data['city'], owner = request.user)
            
            if city_in_db.exists(): #if city entered by user is already in db then redirect to home page
                return redirect('home_page')

            else: 
                instance = form.save(commit=False)
                instance.owner = request.user
                instance.save()
                return redirect('home_page')


    context = {'form':form}
    return render(request, 'city.html', context)


@login_required(login_url='login')
def city(request, city_name):

    try:
        city_name_given = Cities.objects.filter(city = city_name)[0]
        coordinates = coordinates_fun(city_name_given, 2)
        response = get_weather_data(coordinates)

        context = {
            "city_name_given":city_name_given,
            # weather info
            "weather" : response.json()["weather"][0]["main"],
            "weather_description" : response.json()["weather"][0]["description"],
            "current_temperature" : kelvin_to_celsius_conv(response.json()["main"]["temp"]),
            "current_temperature_feels_like" : kelvin_to_celsius_conv(response.json()["main"]["feels_like"]),
            "pressure" : response.json()["main"]["pressure"],
            "humidity" : response.json()["main"]["humidity"],
            "wind_speed" : response.json()["wind"]["speed"]
            }

    except:
        context = {}
        messages.info(request, 'Wystąpił błąd - być może źle wpisałeś nazwę miasta?')
        return redirect('home_page')

    return render(request, 'city_forecast.html', context)


@login_required
def deleteCity(request, city_name):
    
    city_to_delete = Cities.objects.get(city = city_name, owner = request.user)
    
    if request.method == 'POST':
        city_to_delete.delete()
        return redirect('home_page')

    context = {
        "city_to_delete":city_to_delete,
        }

    return render(request, 'delete_city.html', context)


@login_required
def deleteUser(request):

    owner = request.user

    if request.method == 'POST':
        
        try:
            owner.delete()
            messages.success(request, "User has been deleted")
            return redirect('home_page')

        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('home_page')

    context = {
        'owner':owner,
        }

    return render(request, 'delete_user.html', context)



def message(request):

    context = {}

    return render(request, 'message.html', context)