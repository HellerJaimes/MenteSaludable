import os
import sys
import django

# Configuración del entorno Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MenteSaludable.settings')
django.setup()

from main.models import Pregunta

PREGUNTAS = [
    # Emociones (EM)
    {"texto": "¿Cómo te has sentido la mayor parte del tiempo esta semana?", "categoria": "EM", "orden": 1},
    {"texto": "¿Con qué frecuencia te has sentido en paz contigo mismo/a?", "categoria": "EM", "orden": 2},
    {"texto": "¿Has podido disfrutar de las pequeñas cosas de la vida cotidiana?", "categoria": "EM", "orden": 3},
    {"texto": "¿Te has sentido abrumado/a por tus emociones?", "categoria": "EM", "orden": 4},
    {"texto": "¿Has tenido momentos de alegría espontánea?", "categoria": "EM", "orden": 5},
    
    # Energía y Motivación (EN)
    {"texto": "¿Cómo describirías tu nivel de energía al despertar?", "categoria": "EN", "orden": 6},
    {"texto": "¿Has tenido ganas de realizar actividades que te gustan?", "categoria": "EN", "orden": 7},
    {"texto": "¿Te ha costado trabajo empezar tus tareas diarias?", "categoria": "EN", "orden": 8},
    {"texto": "¿Has sentido que 'arrastras los pies' durante el día?", "categoria": "EN", "orden": 9},
    {"texto": "¿Te has sentido satisfecho/a con lo que lograste cada día?", "categoria": "EN", "orden": 10},
    
    # Relaciones (RE)
    {"texto": "¿Te has sentido acompañado/a por las personas importantes en tu vida?", "categoria": "RE", "orden": 11},
    {"texto": "¿Has tenido conflictos que afectaron tu estado de ánimo?", "categoria": "RE", "orden": 12},
    {"texto": "¿Has compartido tiempo de calidad con tus seres queridos?", "categoria": "RE", "orden": 13},
    {"texto": "¿Te has sentido comprendido/a cuando lo necesitabas?", "categoria": "RE", "orden": 14},
    {"texto": "¿Has evitado contacto social cuando normalmente lo disfrutarías?", "categoria": "RE", "orden": 15},
    
    # Hábitos y Cuidado Personal (HB)
    {"texto": "¿Qué tan bien has estado durmiendo?", "categoria": "HB", "orden": 16},
    {"texto": "¿Has mantenido una alimentación que te hace sentir bien?", "categoria": "HB", "orden": 17},
    {"texto": "¿Has hecho alguna actividad física por tu bienestar?", "categoria": "HB", "orden": 18},
    {"texto": "¿Has tenido momentos para relajarte sin distracciones?", "categoria": "HB", "orden": 19},
    {"texto": "¿Te has sentido en armonía con tu cuerpo?", "categoria": "HB", "orden": 20},
    
    # Pensamientos y Perspectiva (PE)
    {"texto": "¿Has tenido pensamientos repetitivos que te molestan?", "categoria": "PE", "orden": 21},
    {"texto": "¿Te has sentido optimista sobre el futuro?", "categoria": "PE", "orden": 22},
    {"texto": "¿Has podido concentrarte en lo que estás haciendo?", "categoria": "PE", "orden": 23},
    {"texto": "¿Te has criticado a ti mismo/a con dureza?", "categoria": "PE", "orden": 24},
    {"texto": "¿Has encontrado significado en tus actividades diarias?", "categoria": "PE", "orden": 25},
    
    # Estrés y Manejo (ES)
    {"texto": "¿Qué tan manejable te han parecido tus responsabilidades?", "categoria": "ES", "orden": 26},
    {"texto": "¿Has tenido momentos de tensión física (mandíbula apretada, hombros tensos)?", "categoria": "ES", "orden": 27},
    {"texto": "¿Has utilizado alguna técnica para calmarte cuando lo necesitabas?", "categoria": "ES", "orden": 28},
    {"texto": "¿Te has sentido capaz de manejar imprevistos?", "categoria": "ES", "orden": 29},
    {"texto": "Al final del día, ¿qué tan satisfecho/a has estado con cómo manejaste los desafíos?", "categoria": "ES", "orden": 30}
]

def poblar_db():
    # Eliminar preguntas existentes para evitar duplicados
    Pregunta.objects.all().delete()
    
    for pregunta_data in PREGUNTAS:
        Pregunta.objects.create(
            texto=pregunta_data['texto'],
            categoria=pregunta_data['categoria'],
            orden=pregunta_data['orden']
        )
    
    print(f"✅ Se han creado {len(PREGUNTAS)} preguntas para el test de salud mental")

if __name__ == '__main__':
    poblar_db()