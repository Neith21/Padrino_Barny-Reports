import uuid
from django.conf import settings
from django.db import models

class Area(models.Model):
    # --- Campos del Modelo ---
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="nombre del área"
    )

    # --- Relaciones ---
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si se elimina el usuario, el campo queda nulo
        null=True,
        blank=True, # Permite que un área no tenga coordinador asignado temporalmente
        related_name='coordinated_area', # Nombre para la relación inversa desde User
        verbose_name="coordinador de área",
        help_text="Usuario asignado como coordinador de esta área."
    )

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        # Devuelve el nombre del área para una representación clara
        return self.name

    class Meta:
        db_table = 'area' # Nombre de la tabla en la base de datos
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['name'] # Ordena los registros por nombre por defecto