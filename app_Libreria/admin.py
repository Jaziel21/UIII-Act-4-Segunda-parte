from django.contrib import admin
from .models import Autor, Libro, Venta, Cliente  # Asegúrate de incluir Cliente si lo creaste

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacionalidad', 'fecha_nacimiento', 'activo')
    search_fields = ('nombre', 'nacionalidad')

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'isbn', 'genero', 'precio', 'stock')
    search_fields = ('titulo', 'isbn')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'libro', 'cantidad', 'total', 'fecha_venta', 'estado')
    list_filter = ('estado',)

# SI AGREGaste el modelo Cliente, añade esto:
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono')
    search_fields = ('nombre', 'correo')
