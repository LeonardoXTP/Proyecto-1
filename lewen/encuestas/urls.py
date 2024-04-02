from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    # Ejemplo: /encuestas/
    path('', views.IndexView.as_view(), name='index'),

    # Ejemplo: /encuestas/5/
    # El valor 'name' tal y como es llamado por la etiqueta de plantilla {% url %}
    path('<int:pk>/', views.DetalleView.as_view(), name='detalle'),

    # Ejemplo: /encuestas/5/resultados/
    path('<int:pk>/resultados/', views.ResultadosView.as_view(), name='resultados'),

    # Ejemplo: /encuestas/5/voto/
    path('<int:pregunta_r_id>/voto/', views.voto, name='voto'),
]