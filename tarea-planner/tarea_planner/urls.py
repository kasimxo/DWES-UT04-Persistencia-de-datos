from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, HomeView, TareasView, CreacionTareasView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('tareas/', TareasView.as_view(), name='tareas'),
    path('tareas/crear/', CreacionTareasView.as_view(), name='create_tarea'),
]
