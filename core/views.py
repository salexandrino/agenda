from django.shortcuts import redirect, render
from core.models import Evento

def lista_eventos(request):
    if request.user.is_authenticated:
        eventos = Evento.objects.filter(usuario=request.user)
    else:
        eventos = Evento.objects.none()
    dados = {'eventos': eventos}
    return render(request, 'agenda.html', dados)


#def index(request):
  #  return redirect('/agenda/')

