from django.db import models

# Create your models here.
"""
Voy a necesitar un alumno y un profesor
Necesitaré:
- Nombre completo
- Email
- Password
- Rol (alumno o profesor)

Como estas cosas son comunes para ambos, voy a hacer un solo modelo con una distinción de rol
"""
class User(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=models.UUIDField, 
        editable=False
        )
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('student', 'Alumno'),
        ('teacher', 'Profesor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.role})"

"""
Para el modelo de tarea, necesito:
- Título
- Descripción
- Fecha de entrega

Como una tarea puede estar asignada un alumno o a varios,
haré una relación ManyToMany con el modelo User
"""
class Task(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=models.UUIDField, 
        editable=False
        )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    assigned_to = models.ManyToManyField(
        User, 
        related_name='tasks',
        blank=True
        )

    def __str__(self):
        return f"{self.title} - Assigned to: {', '.join([user.name for user in self.assigned_to.all()])}"