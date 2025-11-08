from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro,Autor
from django.urls import reverse

# Página de inicio del sistema
def inicio_libreria(request):
    contexto = {
        'titulo': 'Sistema de Administración Libreria AJMG 1194',
    }
    return render(request, 'inicio.html', contexto)

# Agregar autor (muestra formulario y procesa POST)
def agregar_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nacionalidad = request.POST.get('nacionalidad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        biografia = request.POST.get('biografia')
        email = request.POST.get('email')
        activo = True if request.POST.get('activo') == 'on' else False

        Autor.objects.create(
            nombre=nombre,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
            fecha_fallecimiento=fecha_fallecimiento,
            biografia=biografia,
            email=email,
            activo=activo,
        )
        return redirect('ver_autores')

    return render(request, 'autor/agregar_autor.html')

# Ver todos los autores
def ver_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autor/ver_autores.html', {'autores': autores})

# Mostrar formulario de actualización de autor (GET)
def actualizar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/actualizar_autor.html', {'autor': autor})

# Procesar la actualización (POST)
def realizar_actualizacion_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.nombre = request.POST.get('nombre')
        autor.nacionalidad = request.POST.get('nacionalidad')
        
        # CORREGIR: Manejar fechas vacías correctamente
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        autor.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else autor.fecha_nacimiento
        
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento')
        autor.fecha_fallecimiento = fecha_fallecimiento if fecha_fallecimiento else None
        
        autor.biografia = request.POST.get('biografia')
        autor.email = request.POST.get('email') or None  # Permitir email vacío
        autor.activo = True if request.POST.get('activo') == 'on' else False
        
        autor.save()
        return redirect('ver_autores')
    return redirect('actualizar_autor', autor_id=autor_id)

# Borrar autor (confirmación GET + borrado POST)
def borrar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.delete()
        return redirect('ver_autores')
    return render(request, 'autor/borrar_autor.html', {'autor': autor})

def agregar_libro(request):
    if request.method == 'POST':
        try:
            # Procesar formulario manualmente
            titulo = request.POST.get('titulo')
            isbn = request.POST.get('isbn')
            genero = request.POST.get('genero')
            fecha_publicacion = request.POST.get('fecha_publicacion')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            descripcion = request.POST.get('descripcion')
            autores_ids = request.POST.getlist('autores')
            
            # Crear el libro
            libro = Libro.objects.create(
                titulo=titulo,
                isbn=isbn,
                genero=genero,
                fecha_publicacion=fecha_publicacion,
                precio=precio,
                stock=stock,
                descripcion=descripcion
            )
            
            # Manejar relación ManyToMany con autores
            if autores_ids:
                autores = Autor.objects.filter(id__in=autores_ids)
                libro.autores.set(autores)
            
            return redirect('ver_libros')
            
        except Exception as e:
            # En caso de error, mostrar el formulario nuevamente
            autores = Autor.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/agregar_libro.html', {
                'autores': autores,
                'generos': generos,
                'error': 'Error al crear el libro. Verifique los datos.'
            })
    
    # GET request - mostrar formulario
    autores = Autor.objects.filter(activo=True)
    generos = Libro.GENEROS
    return render(request, 'libro/agregar_libro.html', {
        'autores': autores,
        'generos': generos
    })

def ver_libros(request):
    libros = Libro.objects.all().prefetch_related('autores')
    return render(request, 'libro/ver_libros.html', {'libros': libros})

def actualizar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    autores = Autor.objects.filter(activo=True)
    generos = Libro.GENEROS
    
    return render(request, 'libro/actualizar_libro.html', {
        'libro': libro,
        'autores': autores,
        'generos': generos
    })

def realizar_actualizacion_libro(request, libro_id):
    if request.method == 'POST':
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            
            # Actualizar campos
            libro.titulo = request.POST.get('titulo')
            libro.isbn = request.POST.get('isbn')
            libro.genero = request.POST.get('genero')
            libro.fecha_publicacion = request.POST.get('fecha_publicacion')
            libro.precio = request.POST.get('precio')
            libro.stock = request.POST.get('stock')
            libro.descripcion = request.POST.get('descripcion')
            
            libro.save()
            
            # Actualizar relación ManyToMany con autores
            autores_ids = request.POST.getlist('autores')
            if autores_ids:
                autores = Autor.objects.filter(id__in=autores_ids)
                libro.autores.set(autores)
            else:
                # Si no se seleccionaron autores, limpiar la relación
                libro.autores.clear()
            
            return redirect('ver_libros')
            
        except Exception as e:
            # Regresar a la página de actualización con error
            libro = get_object_or_404(Libro, id=libro_id)
            autores = Autor.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/actualizar_libro.html', {
                'libro': libro,
                'autores': autores,
                'generos': generos,
                'error': 'Error al actualizar el libro.'
            })
    
    return redirect('actualizar_libro', libro_id=libro_id)

def borrar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        return redirect('ver_libros')
    
    return render(request, 'libro/borrar_libro.html', {'libro': libro})