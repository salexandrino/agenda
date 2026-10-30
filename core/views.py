from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models import Evento


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')


def submit_login(request):
    if request.method != 'POST':
        return redirect('/login/')

    username = request.POST.get('username')
    password = request.POST.get('password')
    usuario = authenticate(request, username=username, password=password)
    if usuario is not None:
        login(request, usuario)
        return redirect('/agenda/')

    messages.error(request, 'Usuário ou senha inválidos.')
    return redirect('/login/')


@login_required(login_url='/login/')
def lista_eventos(request):
    evento = Evento.objects.filter(usuario=request.user)
    return render(request, 'agenda.html', {'eventos': evento})
