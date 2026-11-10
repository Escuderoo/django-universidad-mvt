from django.urls import path
from . import views

urlpatterns = [
    # Listar estudiantes
    path('web/estudiantes/', views.EstudianteListView.as_view(), name='web_lista_estudiantes'),
    
    # Detalle de estudiante
    path('web/estudiantes/<int:pk>/', views.EstudianteDetailView.as_view(), name='web_detalle_estudiante'),
    
    # Crear estudiante
    path('web/estudiantes/nuevo/', views.EstudianteCreateView.as_view(), name='web_crear_estudiante'),
    
    # Editar estudiante
    path('web/estudiantes/<int:pk>/editar/', views.EstudianteUpdateView.as_view(), name='web_editar_estudiante'),
    
    # Eliminar estudiante
    path('web/estudiantes/<int:pk>/eliminar/', views.EstudianteDeleteView.as_view(), name='web_eliminar_estudiante'),
    
    # Reto Avanzado: Inscribir estudiante a un curso (Relación N:M)
    path('web/estudiantes/<int:pk>/inscribir/', views.InscribirCursoView.as_view(), name='inscribir_curso'),
]