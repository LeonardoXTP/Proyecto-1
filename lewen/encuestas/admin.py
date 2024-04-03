from django.contrib import admin

from .models import Pregunta, Respuesta

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['pregunta_p']}),
        ('Información de le fecha', {'fields': ['fecha'], 'classes': ['collapse'] }),
    ]
    inlines = [RespuestaInline]
    list_display = ('pregunta_p', 'fecha', 'pub_reciente')
    list_filter = ('fecha',)
    search_fields = ('pregunta_p',)

admin.site.register(Pregunta, PreguntaAdmin)