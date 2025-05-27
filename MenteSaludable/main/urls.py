from django.urls import path
from . import views
from .views import logout_view

app_name = 'main'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('test/', views.test_animo, name='test'),
    path('resultados/', views.resultados, name='resultados'),
    path('historial/', views.historial, name='historial'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
]