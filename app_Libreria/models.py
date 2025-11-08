from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Autor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    nacionalidad = models.CharField(max_length=50, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    fecha_fallecimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de fallecimiento")
    biografia = models.TextField(verbose_name="Biografía", help_text="Breve biografía del autor")
    # CAMBIA ESTA LÍNEA - agregar blank=True:
    email = models.EmailField(verbose_name="Email de contacto", blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name="Autor activo")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
    ]
    titulo = models.CharField(max_length=200, verbose_name="Título del libro")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    genero = models.CharField(max_length=3, choices=GENEROS, verbose_name="Género")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    autores = models.ManyToManyField(Autor, related_name='libros', verbose_name="Autores")

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    def disponible(self):
        return self.stock > 0

class Venta(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
        ('DEV', 'Devuelta'),
    ]
    fecha_venta = models.DateTimeField(default=timezone.now, verbose_name="Fecha de venta")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad vendida")
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio unitario")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta")
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN', verbose_name="Estado de la venta")
    cliente_nombre = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    cliente_email = models.EmailField(verbose_name="Email del cliente")
    libro = models.ForeignKey(
        Libro, on_delete=models.PROTECT, related_name='ventas', verbose_name="Libro vendido"
    )

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta #{self.id} - {self.libro.titulo}"

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

