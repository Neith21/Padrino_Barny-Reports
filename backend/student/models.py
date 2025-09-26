from django.conf import settings
from django.db import models
from career.models import Career

class Student(models.Model):
    # --- Campos del Modelo ---
    first_name = models.CharField(
        max_length=150,
        verbose_name="nombres del estudiante"
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="apellidos del estudiante"
    )
    carnet = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="carnet"
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True, # El email es único si se proporciona, pero no es obligatorio
        blank=True,
        verbose_name="correo electrónico"
    )

    # --- Relaciones ---
    career = models.ForeignKey(
        Career,
        on_delete=models.PROTECT, # Evita que se pueda borrar una carrera si tiene estudiantes
        related_name='students',
        verbose_name="carrera"
    )

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        # Devuelve una representación completa y clara del estudiante
        return f"{self.first_name} {self.last_name} ({self.carnet})"

    class Meta:
        db_table = 'student'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['last_name', 'first_name'] # Ordena por apellido y luego por nombre