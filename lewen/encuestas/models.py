from django.db import models

class Pregunta(models.Model):
    pregunta_p = models.CharField(max_length=200)
    fecha = models.DateTimeField("fecha de publicación")

class Respuestas(models.Model):
    pregunta_r = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)