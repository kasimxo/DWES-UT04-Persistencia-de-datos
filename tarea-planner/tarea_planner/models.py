from django.db import models

# Create your models here.
"""
Voy a necesitar un alumno y un profesor
Necesitaré:
- Nombre completo
- Email
- Password
- Rol (alumno o profesor)
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
        return f"{self.full_name} ({self.role})"