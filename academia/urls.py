from django.contrib import admin
from django.urls import path, include
from cursos.views import MiLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta de login personalizada que dispara el mensaje flash
    path('accounts/login/', MiLoginView.as_view(), name='login'),
    
    # Rutas de la app cursos
    path('', include('cursos.urls')),
]
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView  # 1. Agrega esta importación arriba
from cursos.views import MiLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Tus rutas de autenticación
    path('accounts/login/', MiLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),  # 2. Agrega esta línea en medio
    
    # Tus rutas de cursos
    path('', include('cursos.urls')),
]