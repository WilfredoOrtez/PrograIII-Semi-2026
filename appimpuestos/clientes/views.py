from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hola_mundo(request):
    return HttpResponse("Hola Mundo, bienvenidos a program III")

def saludoNombre(request, nombre, edad):
    return HttpResponse(f"Hola {nombre}, Bienvenido a program III, tienes {edad} años.")

def index(request):
    return render(request, 'index.html')