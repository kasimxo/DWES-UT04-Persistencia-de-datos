from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from ..models import User, Task

class TareasView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        if user.role == 'student':
            tareas = Task.objects.filter(Q(assigned_to=user) | Q(created_by=user)).distinct().order_by('-due_date')
        else:
            tareas = Task.objects.filter(created_by=user).order_by('-due_date')
        return render(request, "tareas/tareas.html", {"tareas": tareas, "page_title": "Tareas"})

class CreacionTareasView(LoginRequiredMixin, View):
    
    def get(self, request):
        users = User.objects.filter(role='student').exclude(id=request.user.id)
        return render(
            request, 
            "tareas/crear_tarea.html", 
            {"users": users,
             "page_title": "Crear Tarea"})

    def post(self, request):
        print("Datos recibidos en el POST:")
        print(request.POST)
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        due_date = request.POST.get("fecha_vencimiento")
        is_evaluable = request.POST.get("es_evaluable")
        grupal = request.POST.get("grupal")
        assigned_students_ids = request.POST.getlist("usuarios_asignados")

        if not all([titulo, descripcion, due_date, assigned_students_ids]):
            messages.error(request, "Los campos título, descripción, fecha de vencimiento y usuarios asignados son obligatorios.")
            return redirect("create_tarea")
        

        fecha_vencimiento = datetime.strptime(due_date, "%Y-%m-%d").date()

        if fecha_vencimiento < timezone.now().date():
            messages.error(request, "La fecha de vencimiento no puede ser anterior a la fecha actual.")
            return redirect("create_tarea")
        
        """
        El problema que estamos teniendo ahoramismo son los assigned students ids, que no son correctos
        vamos a ver primero que nos llega y lo fixeamos

        PREGUNTA:
        Si es un estudiante el que crea la tarea, no debería tenerla asignada a sí mismo?
        """
        
        try:
            tarea = Task(
                title=titulo,
                description=descripcion,
                due_date=due_date,
                is_evaluable=bool(is_evaluable),
                created_by=request.user,
            )
            tarea.save()
            tarea.assigned_to.set(User.objects.filter(id__in=assigned_students_ids))
            messages.success(request, "Tarea creada con éxito.")
            print(f"Tarea '{titulo}' creada con éxito.")
        except Exception as e:
            messages.error(request, f"Error al crear la tarea: {str(e)}")
            print(f"Error al crear la tarea: {str(e)}")
            return redirect("create_tarea")

        return redirect("tareas")
