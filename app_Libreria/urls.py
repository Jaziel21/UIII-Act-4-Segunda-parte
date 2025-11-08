from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_libreria, name='inicio_libreria'),
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/', views.ver_autores, name='ver_autores'),
    path('autores/editar/<int:autor_id>/', views.actualizar_autor, name='actualizar_autor'),
    path('autores/editar/guardar/<int:autor_id>/', views.realizar_actualizacion_autor, name='realizar_actualizacion_autor'),
    path('autores/borrar/<int:autor_id>/', views.borrar_autor, name='borrar_autor'),
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/', views.ver_libros, name='ver_libros'),
    path('libros/editar/<int:libro_id>/', views.actualizar_libro, name='actualizar_libro'),
    path('libros/editar/guardar/<int:libro_id>/', views.realizar_actualizacion_libro, name='realizar_actualizacion_libro'),
    path('libros/borrar/<int:libro_id>/', views.borrar_libro, name='borrar_libro'),
]