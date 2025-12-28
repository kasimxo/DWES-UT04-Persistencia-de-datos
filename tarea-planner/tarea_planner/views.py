from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.views import View
from .models import User

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
        return render(request, "home/home.html")

class TareasView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "tareas/tareas.html")
    
class CreacionTareasView(LoginRequiredMixin, View):
    
    def get(self, request):
        users = User.objects.filter(role='student').exclude(id=request.user.id)
        return render(
            request, 
            "tareas/crear_tarea.html", 
            {"users": users})

    def post(self, request):
        """
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")

        if not all([titulo, descripcion]):
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, "tareas/crear_tarea.html")

        # Aquí se guardaría la tarea en la base de datos (lógica no implementada)
        messages.success(request, "Tarea creada con éxito.")
        """
        return redirect("tareas")