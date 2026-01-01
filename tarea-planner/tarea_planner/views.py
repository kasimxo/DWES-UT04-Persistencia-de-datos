from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic.detail import DetailView
from .models import User, Task

User = get_user_model()

class RegisterView(View):

    def get(self, request):
        return render(request, "register/register.html")
    
    def post(self, request):

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not all([first_name, last_name, email, password, role]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, "register/register.html")

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            user.save()
            messages.success(request, "Usuario registrado con éxito.")
            print(f"Usuario {email} {password} registrado con éxito.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error al registrar el usuario: {str(e)}")
            return render(request, "register/register.html")


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("tareas")
        return render(request, "home/home.html", {"page_title": "Tarea Planner"})

class TareasView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "tareas/tareas.html", {"page_title": "Tareas"})

class CreacionTareasView(LoginRequiredMixin, View):
    
    def get(self, request):
        users = User.objects.filter(role='student').exclude(id=request.user.id)
        return render(
            request, 
            "tareas/crear_tarea.html", 
            {"users": users,
             "page_title": "Crear Tarea"})

    def post(self, request):

        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        due_date = request.POST.get("fecha_vencimiento")
        is_evaluable = request.POST.get("es_evaluable")
        grupal = request.POST.get("grupal")
        assigned_students_ids = request.POST.getlist("alumnos_asignados") # Esto no está implementado todavía

        if not all([titulo, descripcion, due_date]):
            messages.error(request, "Los campos título, descripción y fecha de vencimiento son obligatorios.")
            return render(request, "tareas/crear_tarea.html")
        
        try:
            tarea = Task(
                titulo=titulo,
                descripcion=descripcion,
                due_date=due_date,
                is_evaluable=bool(is_evaluable),
                grupal=bool(grupal),
                created_by=request.user,
                assigned_to=User.objects.filter(id__in=assigned_students_ids)
            )
            tarea.save()
            messages.success(request, "Tarea creada con éxito.")
        except:
            messages.error(request, "Error al crear la tarea.")
        
        return redirect("tareas")

class ListadoUsuariosView(LoginRequiredMixin, View):

    def get(self, request):
        users = User.objects.all()
        return render(request, "usuarios/listado_usuarios.html", {"users": users, "page_title": "Listado de Usuarios"})
    
class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "usuarios/perfil_usuario.html"
    context_object_name = "usuario"
    pk_url_kwarg = "user_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Perfil de {self.object.get_full_name()}"
        return context