from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    # Ejemplo: /encuestas/
    path('', views.index, name='index'),

    # Ejemplo: /encuestas/5/
    # El valor 'name' tal y como es llamado por la etiqueta de plantilla {% url %}
    path('detalle/<int:pregunta_r_id>/', views.detalle, name='detalle'),

    # Ejemplo: /encuestas/5/resultados/
    path('<int:pregunta_r_id>/resultados/', views.resultados, name='resultados'),

    # Ejemplo: /encuestas/5/voto/
    path('<int:pregunta_r_id>/voto/', views.voto, name='voto'),
]