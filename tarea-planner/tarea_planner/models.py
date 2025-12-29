import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ROLE_CHOICES = [
        ('student', 'Alumno'),
        ('teacher', 'Profesor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

"""
Para el modelo de tarea, necesito:
- Título
- Descripción
- Fecha de entrega

Como una tarea puede estar asignada un alumno o a varios,
haré una relación ManyToMany con el modelo User

Voy a meter también un campo de "Respuesta"
Este campo sólo see podrá rellenar en la "edición" de la tarea por el alumno
También voy a meter un campo de evaluable, que será un boolean
Si la tarea es evaluable, una vez sea entregada, le aparecerá al profesor para poder ponerla apta/no apta
También voy a meter un campo de evaluación, que será nulable (para las tareas no evaluables) o apto/no apto
Y por último, la fecha de entrega, para que el alumno pueda darla por "finalizada/entregada"

Una tarea finalizada/entregada no se podrá editar por el alumno, sólo se podrá evaluar por el profesor
"""
class Task(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=models.UUIDField, 
        editable=False
        )
    title = models.CharField(max_length=200)
    description = models.TextField()
    response = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    assigned_to = models.ManyToManyField(
        User, 
        related_name='tasks',
        blank=True
        )
    is_evaluable = models.BooleanField(default=False)
    EVALUATION_CHOICES = [
        ('apto', 'Apto'),
        ('no_apto', 'No Apto'),
    ]
    evaluation = models.CharField(
        max_length=10, 
        choices=EVALUATION_CHOICES, 
        blank=True, 
        null=True
        )
    finished_at = models.DateTimeField(blank=True, null=True)   

    def __str__(self):
        return f"{self.title} - Assigned to: {', '.join([user.name for user in self.assigned_to.all()])}"