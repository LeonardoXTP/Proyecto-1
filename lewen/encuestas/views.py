from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Pregunta, Respuesta

class IndexView(generic.ListView):
    template_name = 'encuestas/pagina1.html'
    context_object_name = "ultimas_preguntas"

    def get_queryset(self):
        # Devuelve las últimas 5 preguntas publicadas
        # sin incluir los que se publiquen en el futuro
        return Pregunta.objects.filter(fecha__lte=timezone.now()).order_by('-fecha')[
            :5
        ]

class DetalleView(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/detalle.html'

    def get_queryset(self):
        """
        Excluye las preguntas que aún no se han publicado.
        """
        return Pregunta.objects.filter(fecha__lte=timezone.now())
    
class ResultadosView (generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/resultados.html'

def voto(request, pregunta_r_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_r_id)
    try:
        opcion_seleccionada = pregunta.respuesta_set.get(pk=request.POST['opcion'])
    except (KeyError, Respuesta.DoesNotExist):
        # Vuelve a mostrar el formulario de votación de preguntas.
        return render(
            request,
            'encuestas/detalle.html',
            {
                "pregunta": pregunta,
                "msj_error": "Debes seleccionar una opción.",
            }
        )
    else:
        opcion_seleccionada.votos = F("votos") + 1
        opcion_seleccionada.save()
        # Siempre devuelve un HttpResponseRedirect después de tratar con éxito los datos POST.
        # Esto evita que los datos se publiquen dos veces si un usuario pulsa el botón Atrás.
        return HttpResponseRedirect(reverse('encuestas:resultados', args=(pregunta.id,)))