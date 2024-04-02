import datetime
from django.db import models
from django.utils import timezone

class Pregunta(models.Model):
    pregunta_p = models.CharField(max_length=200)
    fecha = models.DateTimeField("fecha de publicación")

    def __str__(self):
        return self.pregunta_p
    
    def pub_reciente(self):
        ahora = timezone.now()
        return ahora - datetime.timedelta(days=1) <= self.fecha <= ahora

class Respuesta(models.Model):
    pregunta_r = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.respuesta