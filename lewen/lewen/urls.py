from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('encuestas/', include('encuestas.urls')),
    path('admin/', admin.site.urls),
]
