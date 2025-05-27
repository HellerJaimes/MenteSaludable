from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Pregunta, Evaluacion, Respuesta
from .forms import TestForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .analisis import analizar_resultados

def inicio(request):
    """Vista para la página de inicio con contexto enriquecido"""
    context = {
        'titulo': 'Bienvenido a MenteSaludable',
        'descripcion': 'Sistema de evaluación y seguimiento de tu bienestar emocional',
        'ultima_evaluacion': None
    }
    
    if request.user.is_authenticated:
        context['ultima_evaluacion'] = Evaluacion.objects.filter(
            usuario=request.user
        ).order_by('-fecha').first()
    
    return render(request, 'main/inicio.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Cuenta creada correctamente. Inicia sesión.')
            return redirect('main:inicio')
    else:
        form = UserCreationForm()
    return render(request, 'main/registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            auth_login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.username}!")
            return redirect('main:inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'main/registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('main:login')


@login_required
def test_animo(request):
    preguntas = Pregunta.objects.all().order_by('orden')
    
    if not preguntas.exists():
        messages.warning(request, "El test no está disponible temporalmente")
        return redirect('inicio')
    
    if request.method == 'POST':
        form = TestForm(request.POST, preguntas=preguntas)
        if form.is_valid():
            try:
                evaluacion = Evaluacion.objects.create(
                    usuario=request.user,
                    puntuacion_total=0,
                    mensaje_personalizado="",
                    nivel_actual=0,
                    analisis_categorias={}
                )
                
                resultados = procesar_respuestas(form, preguntas, request.user, evaluacion)
                
                evaluacion.puntuacion_total = resultados['promedio']
                evaluacion.mensaje_personalizado = resultados['mensaje']
                evaluacion.nivel_actual = resultados['nivel']
                evaluacion.analisis_categorias = resultados['analisis_categorias']
                evaluacion.recomendaciones = resultados['recomendaciones']  # **Guarda las recomendaciones**
                evaluacion.save()
                
                messages.success(request, "¡Evaluación completada con éxito!")
                return redirect('main:resultados')
                
            except Exception as e:
                messages.error(request, f"Ocurrió un error: {str(e)}")
                return redirect('main:inicio')

    else:
        form = TestForm(preguntas=preguntas)
    
    context = {
        'form': form,
        'preguntas': preguntas,
        'escala': [
            {'valor': 1, 'descripcion': 'Muy mal - Necesito ayuda'},
            {'valor': 2, 'descripcion': 'Mal - Tengo dificultades'},
            {'valor': 3, 'descripcion': 'Regular - Podría mejorar'},
            {'valor': 4, 'descripcion': 'Bien - Me siento bastante bien'},
            {'valor': 5, 'descripcion': 'Excelente - Me siento genial'}
        ]
    }
    return render(request, 'main/test.html', context)

def procesar_respuestas(form, preguntas, usuario, evaluacion):
    total = 0
    respuestas = []
    categorias = {}
    
    for pregunta in preguntas:
        valor = int(form.cleaned_data[f'pregunta_{pregunta.id}'])
        total += valor
        respuestas.append({
            'pregunta': pregunta.texto,
            'valor': valor,
            'categoria': pregunta.get_categoria_display()
        })
        
        # Guardar la respuesta en la base de datos
        Respuesta.objects.create(
            usuario=usuario,
            pregunta=pregunta,
            valor=valor,
            evaluacion=evaluacion
        )
        
        # Análisis por categorías
        if pregunta.categoria not in categorias:
            categorias[pregunta.categoria] = {
                'suma': 0,
                'total': 0,
                'nombre': pregunta.get_categoria_display()
            }
        categorias[pregunta.categoria]['suma'] += valor
        categorias[pregunta.categoria]['total'] += 1
    
    promedio = total / len(preguntas)
    nivel = round(promedio)
    
    analisis_categorias = {
        cat: {
            'nombre': datos['nombre'],
            'promedio': round(datos['suma'] / datos['total'], 2),
            'necesita_mejorar': (datos['suma'] / datos['total']) < 3
        }
        for cat, datos in categorias.items()
    }

    # Crear un dict con puntuaciones de categorías para analizar_resultados
    puntuaciones = {
        cat: round(datos['suma'] / datos['total'], 2)
        for cat, datos in categorias.items()
    }
    
    recomendaciones_texto = analizar_resultados(puntuaciones)
    
    return {
        'promedio': round(promedio, 2),
        'nivel': nivel,
        'mensaje': generar_mensaje(usuario.first_name or usuario.username, promedio, analisis_categorias),
        'analisis_categorias': analisis_categorias,
        'recomendaciones': recomendaciones_texto
    }


def generar_mensaje(nombre, promedio, analisis_categorias):
    """Genera mensajes personalizados basados en los resultados"""
    nivel = round(promedio)
    
    # Lista con nombres de categorías que necesitan mejorar
    problemas = [cat['nombre'] for cat in analisis_categorias.values() if cat.get('necesita_mejorar')]
    
    mensajes = {
        1: f"{nombre}, recomendamos buscar ayuda profesional inmediatamente. Detectamos dificultades en: {', '.join(problemas)}.",
        2: f"{nombre}, hay áreas significativas que mejorar, especialmente en: {', '.join(problemas)}. Te sugerimos buscar apoyo.",
        3: f"{nombre}, vas bien pero deberías trabajar en: {', '.join(problemas) if problemas else 'algunos aspectos'}.",
        4: f"{nombre}, estás en buen estado. {'Sigue cuidando especialmente: ' + ', '.join(problemas) + '.' if problemas else '¡Sigue así!'}",
        5: f"{nombre}, ¡excelente estado emocional en todas las áreas! Sigue con tus buenos hábitos."
    }
    
    # Devuelve mensaje basado en nivel o mensaje genérico por defecto
    return mensajes.get(nivel, "Hemos procesado tus resultados. Revisa tu evaluación.")

@login_required
def resultados(request):
    """Vista para mostrar resultados con manejo de casos edge"""
    evaluacion = Evaluacion.objects.filter(
        usuario=request.user,
        fecha__date=timezone.now().date()
    ).order_by('-fecha').first()
    
    if not evaluacion:
        messages.warning(request, "No has completado ninguna evaluación hoy")
        return redirect('main:test')

    evaluaciones_hoy = Evaluacion.objects.filter(
        usuario=request.user,
        fecha__date=timezone.now().date()
    ).order_by('-fecha')
    
    if evaluaciones_hoy.count() > 1:
        messages.info(request, "Has completado varias evaluaciones hoy. Mostrando la más reciente.")
    
    # La evaluación guardó las recomendaciones en mensaje_personalizado?
    # O mejor pasar las recomendaciones guardadas:
    recomendaciones = getattr(evaluacion, 'recomendaciones', None)
    if not recomendaciones:
        # Si no hay recomendaciones guardadas, puedes generarlas con la función:
        recomendaciones = analizar_resultados(evaluacion.analisis_categorias or {})
    
    context = {
        'evaluacion': evaluacion,
        'categorias': evaluacion.analisis_categorias,
        'recomendaciones': recomendaciones,
        'recomendaciones_generales': [
            "Realiza ejercicios de respiración diarios",
            "Mantén una rutina de sueño consistente",
            "Practica gratitud diariamente"
        ]
    }
    return render(request, 'main/resultados.html', context)

    

@login_required
def historial(request):
    """Vista para mostrar el historial de evaluaciones"""
    evaluaciones = Evaluacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:30]  # Últimas 30 evaluaciones
    
    if not evaluaciones.exists():
        messages.info(request, "Aún no has completado ninguna evaluación")
        return redirect('main:test')
    
    # Estadísticas básicas
    promedio_general = sum(e.puntuacion_total for e in evaluaciones) / len(evaluaciones)
    
    context = {
        'evaluaciones': evaluaciones,
        'promedio_general': round(promedio_general, 2),
        'total_evaluaciones': len(evaluaciones),
        'mejor_evaluacion': max(evaluaciones, key=lambda x: x.puntuacion_total),
        'peor_evaluacion': min(evaluaciones, key=lambda x: x.puntuacion_total)
    }
    
    return render(request, 'main/historial.html', context)