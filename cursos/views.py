from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q  # <-- ¡Importante para los filtros de búsqueda!
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import EstudianteForm
from .models import Curso, Estudiante


# 1. LISTA DE ESTUDIANTES (Paginada y con Buscador por Objetos Q)
class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'cursos/estudiantes_lista.html'
    context_object_name = 'estudiantes'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Captura el parámetro ?q= de la URL

        if query:
            # Filtra por nombre OR apellido OR matrícula
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(matricula__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Envía el término de búsqueda a la plantilla para conservar el texto en el input
        context['query'] = self.request.GET.get('q', '')
        return context


# 2. DETALLE DE ESTUDIANTE (Incluye todos los cursos para el select del reto N:M)
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'cursos/estudiante_detalle.html'
    context_object_name = 'estudiante'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_los_cursos'] = Curso.objects.all()
        return context


# 3. CREAR ESTUDIANTE (Protegido + Mensaje Flash)
class EstudianteCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = (
        '¡El estudiante %(nombre)s %(apellido)s fue registrado con éxito!'
    )


# 4. EDITAR ESTUDIANTE
class EstudianteUpdateView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'cursos/estudiante_formulario.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    success_message = (
        '¡Los datos del estudiante %(nombre)s fueron actualizados correctamente!'
    )


# 5. ELIMINAR ESTUDIANTE
class EstudianteDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudiante
    template_name = 'cursos/estudiante_confirm_delete.html'
    success_url = reverse_lazy('web_lista_estudiantes')
    context_object_name = 'estudiante'

    def delete(self, request, *args, **kwargs):
        estudiante = self.get_object()
        messages.warning(
            self.request,
            f'El estudiante {estudiante.nombre} {estudiante.apellido} fue eliminado.',
        )
        return super().delete(request, *args, **kwargs)


# 6. RETO AVANZADO: Lógica ORM para inscribir un estudiante a un curso (Relación N:M)
class InscribirCursoView(LoginRequiredMixin, View):

    def post(self, request, pk):
        estudiante = get_object_or_404(Estudiante, pk=pk)
        curso_id = request.POST.get('curso_id')

        if curso_id:
            curso = get_object_or_404(Curso, id=curso_id)
            estudiante.cursos.add(curso)
            messages.success(
                request,
                f'Estudiante inscrito en el curso "{curso.nombre}" con éxito.',
            )

        return redirect('web_detalle_estudiante', pk=pk)


# 7. VISTA DE LOGIN
class MiLoginView(LoginView):
    template_name = 'cursos/login.html'