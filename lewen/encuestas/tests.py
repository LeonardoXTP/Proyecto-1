import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Pregunta

def crear_pregunta(pregunta_p, dias):
    """
    Crea una pregunta con el `texto_de_la_pregunta` dado y publicada
    el número de `días` dado de diferencia hasta ahora (negativo para
    preguntas publicadas en el pasado, positivo para preguntas que
    aún no han sido publicadas).
    """
    tiempo = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(pregunta_p=pregunta_p, fecha=tiempo)

class PreguntaIndexViewTests(TestCase):
    def test_no_preguntas(self):
        """
        Si no existen preguntas, se muestra un mensaje apropiado.
        """
        resp = self.client.get(reverse('encuestas:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No hay encuestas disponibles.')
        self.assertQuerysetEqual(resp.context['ultimas_preguntas'], [])

    def test_preguntas_pasadas(self):
        """
        Las preguntas con fecha de publicación anterior se muestran
        en la página de índice.
        """
        pregunta = crear_pregunta(pregunta_p="Pregunta antigua", dias=-30)
        resp = self.client.get(reverse('encuestas:index'))
        self.assertQuerySetEqual(
            resp.context['ultimas_preguntas'],
            [pregunta],
        )

    def test_preguntas_futuras(self):
        """
        Las preguntas con fecha de publicación en el futuro no se
        muestran en la página de índice.
        """
        crear_pregunta(pregunta_p="Pregunta futura", dias=30)
        resp = self.client.get(reverse('encuestas:index'))
        self.assertContains(resp, 'No hay encuestas disponibles.')
        self.assertQuerysetEqual(resp.context['ultimas_preguntas'], [])

    def test_preguntas_futuras_y_pasadas(self):
        """
        Aunque existan preguntas pasadas y futuras, sólo se muestran
        las preguntas pasadas. pasadas.
        """
        pregunta = crear_pregunta(pregunta_p="Pregunta antigua", dias=-30)
        crear_pregunta(pregunta_p="Pregunta futura", dias=30)
        resp = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(
            resp.context['ultimas_preguntas'],
            [pregunta],
        )

    def test_dos_preguntas_pasadas(self):
        """
        La página de índice de preguntas puede mostrar varias preguntas.
        """
        pregunta1 = crear_pregunta(pregunta_p="Pregunta antigua 1", dias=-30)
        pregunta2 = crear_pregunta(pregunta_p="Pregunta antigua 2", dias=-5)
        resp = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(
            resp.context['ultimas_preguntas'],
            [pregunta1, pregunta2],
        )

class PreguntaDetailViewTests(TestCase):
    def test_pregunta_futura(self):
        """
        La vista detallada de una pregunta con fecha de publicación
        en el futuro devuelve un 404 no encontrado.
        """
        pregunta_futura = crear_pregunta(pregunta_p="Pregunta futura", dias=5)
        url = reverse('encuestas:detalle', args=(pregunta_futura.id,))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_pregunta_pasada(self):
        """
        La vista detallada de una pregunta con fecha de publicación
        en el pasado muestra el texto de la pregunta.
        """
        pregunta_pasada = crear_pregunta(pregunta_p="Pregunta pasada", dias=-5)
        url = reverse('encuestas:detalle', args=(pregunta_pasada.id,))
        resp = self.client.get(url)
        self.assertContains(resp, pregunta_pasada.pregunta_p)

class PreguntaModelTests(TestCase):
    
    def test_pub_reciente_con_pregunta_antigua(self):
        """
        pub_reciente() devuelve False para las preguntas cuya 
        fecha de publicación es anterior a 1 día.
        """

        tiempo = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pregunta_antigua = Pregunta(fecha=tiempo)
        self.assertIs(pregunta_antigua.pub_reciente(), False)

    def test_pub_reciente_con_pregunta_reciente(self):
        """
        pub_reciente() devuelve True para las preguntas cuya
        fecha de publicación esté dentro del último día.
        """
        
        tiempo = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta_reciente = Pregunta(fecha=tiempo)
        self.assertIs(pregunta_reciente.pub_reciente(), True)