from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Pregunta(models.Model):
    CATEGORIAS = [
        ('EM', 'Emociones'),
        ('HB', 'Hábitos'),
        ('EN', 'Energía'),
        ('CO', 'Comportamiento'),
        ('RE', 'Relaciones'),
        ('PE', 'Pensamiento y perspectiva'),
        ('ES', 'Estres y Manejo')
    ]
    
    texto = models.TextField(verbose_name="Texto de la pregunta")
    categoria = models.CharField(
        max_length=2,
        choices=CATEGORIAS,
        default='EM',
        verbose_name="Categoría"
    )
    orden = models.PositiveIntegerField(
        unique=True,
        verbose_name="Orden de aparición"
    )
    
    class Meta:
        ordering = ['orden']
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
    
    def __str__(self):
        return f"{self.get_categoria_display()}: {self.texto[:50]}..."

class Evaluacion(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evaluaciones',
        verbose_name="Usuario"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de evaluación"
    )
    
    # Resultados generales
    puntuacion_total = models.FloatField(
        verbose_name="Puntuación total",
        help_text="Promedio de todas las respuestas"
    )
    
    # Análisis por categorías (usamos JSONField para flexibilidad)
    analisis_categorias = models.JSONField(
        verbose_name="Análisis por categorías",
        help_text="Detalles del resultado por categoría",
        default=dict
    )
    
    mensaje_personalizado = models.TextField(
        verbose_name="Mensaje personalizado"
    )
    recomendaciones = models.TextField(blank=True, default="")
    
    NIVELES = [
        (1, 'Requiere atención profesional inmediata'),
        (2, 'Necesita mejorar significativamente'),
        (3, 'Estado regular con áreas a mejorar'),
        (4, 'Buen estado con pequeños ajustes'),
        (5, 'Excelente estado emocional')
    ]
    nivel_actual = models.IntegerField(
        choices=NIVELES,
        verbose_name="Nivel actual"
    )
    
    class Meta:
        verbose_name = "Evaluación"
        verbose_name_plural = "Evaluaciones"
        ordering = ['-fecha']
        get_latest_by = 'fecha'
    
    def __str__(self):
        return f"Evaluación de {self.usuario.username} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    def get_promedio_categoria(self, categoria):
        return self.analisis_categorias.get(categoria, {}).get('promedio', 0)
    
    @property
    def categorias_con_problemas(self):
        return [cat for cat, datos in self.analisis_categorias.items() 
                if datos.get('necesita_mejorar', False)]

class Respuesta(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name="Usuario"
    )
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name="Pregunta"
    )
    valor = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Valor de respuesta",
        help_text="Escala del 1 (peor) al 5 (mejor)"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de respuesta"
    )
    evaluacion = models.ForeignKey(
        Evaluacion,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name="Evaluación asociada",
        null=True,  # Permite que el campo esté vacío al principio
        blank=True,
    )
    
    class Meta:
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"
        unique_together = ('usuario', 'pregunta', 'evaluacion')
        ordering = ['-fecha', 'pregunta__orden']
    
    def __str__(self):
        return f"{self.usuario.username}: {self.pregunta.texto[:30]}... ({self.valor}/5)"
