from django.conf import settings
from django.db import models

class Career(models.Model):
    # --- Campos del Modelo ---
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="career name"
    )

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'career'
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'
        ordering = ['name']