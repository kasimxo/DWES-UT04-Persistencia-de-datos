from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.views import View
from .models import User

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
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            user.save()
            messages.success(request, "Usuario registrado con éxito.")
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