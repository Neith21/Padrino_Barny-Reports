from django.conf import settings
from django.db import models

class Subject(models.Model):
    # --- Campos del Modelo ---
    name = models.CharField(
        max_length=150,
        verbose_name="subject name"
    )
    section = models.CharField(
        max_length=10,
        verbose_name="section"
    )

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        return f"{self.name} - Section: {self.section}"

    class Meta:
        db_table = 'subject'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        # Esta es la restricción clave para evitar que se repita un tema con la misma sección.
        constraints = [
            models.UniqueConstraint(fields=['name', 'section'], name='unique_subject_section')
        ]
        ordering = ['name', 'section']
