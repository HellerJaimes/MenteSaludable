from django.contrib import admin
from .models import Pregunta, Respuesta, Evaluacion

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'categoria', 'orden')
    list_filter = ('categoria',)
    search_fields = ('texto',)

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'valor', 'fecha')
    list_filter = ('valor', 'fecha')
    search_fields = ('usuario__username', 'pregunta__texto')

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'puntuacion_total', 'nivel_actual')
    list_filter = ('nivel_actual', 'fecha')
    search_fields = ('usuario__username', 'mensaje_personalizado')