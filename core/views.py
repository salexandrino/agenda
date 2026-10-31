from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    eventos = Evento.objects.filter(usuario=request.user)
    dados = {'eventos': eventos}
    return render(request, 'agenda.html', dados)


@login_required(login_url = '/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = get_object_or_404(Evento, id=id_evento, usuario=request.user)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.method != 'POST':
        return redirect('agenda')

    titulo = request.POST.get('titulo', '').strip()
    data_evento = request.POST.get('data_evento')
    if not titulo or not data_evento:
        messages.error(request, 'Preencha o título e a data do evento.')
        return redirect('evento')

    id_evento = request.POST.get('id_evento')
    if id_evento:
        evento = get_object_or_404(Evento, id=id_evento, usuario=request.user)
        evento.titulo = titulo
        evento.data_evento = data_evento
        evento.descricao = request.POST.get('descricao') or ''
        evento.save()
    else:
        Evento.objects.create(
            titulo=titulo,
            data_evento=data_evento,
            descricao=request.POST.get('descricao') or '',
            usuario=request.user,
        )

    return redirect('agenda')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=id_evento, usuario=request.user)
        evento.delete()
    return redirect('agenda')

