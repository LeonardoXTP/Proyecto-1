from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Pregunta, Respuesta
from django.template import loader

def index(request):
    ultimas_preguntas = Pregunta.objects.order_by("-fecha")[:5]
    context = {
        'ultimas_preguntas': ultimas_preguntas,
    }
    return render(request, 'encuestas/pagina1.html', context)

def detalle(request, pregunta_r_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_r_id)
    return render(request, 'encuestas/detalle.html', {'pregunta': pregunta})

def resultados(request, pregunta_r_id):
    res = "Estás viendo las respuestas de la pregunta %s."
    return HttpResponse(res % pregunta_r_id)

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