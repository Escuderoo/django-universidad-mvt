from django.contrib import admin
from .models import Curso, Profesor, Estudiante

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'profesor')
    search_fields = ('nombre', 'codigo')
    # NOTA: Si tenías 'filter_horizontal' aquí apuntando a un campo que no es ManyToMany, 
    # bórralo o asegúrate de que apunte solo a campos de tipo ManyToMany.

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'matricula')
    search_fields = ('nombre', 'apellido', 'matricula')
    filter_horizontal = ('cursos',) # Aquí sí es válido porque 'cursos' es ManyToMany