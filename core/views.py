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
    usuario = request.user
    evento = Evento.objects.filter(usuario=request.user)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url = '/login/')
def evento(request):
    return render(request, 'evento.html')


@login_required
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        Evento.objects.create(titulo=titulo,
                              data_evento= data_evento,
                              descricao=descricao,
                              usuario=usuario)

    return redirect('/')

