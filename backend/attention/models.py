from django.conf import settings
from django.db import models
from student.models import Student
from subject.models import Subject

class Attention(models.Model):
    # --- Definición de Opciones ---
    class ChannelChoices(models.TextChoices):
        EMAIL = 'EMAIL', 'Correo Electrónico'
        WHATSAPP = 'WHATSAPP', 'WhatsApp'
        IN_PERSON = 'IN_PERSON', 'Presencial'
        OTHER = 'OTHER', 'Otro'

    # --- Relaciones ---
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Si se borra el docente, la atención no se pierde, solo se desvincula
        null=True,
        related_name='given_attentions',
        verbose_name="docente"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL, # Si se borra el estudiante no se pierde, solo se desvincula
        null=True,
        related_name='received_attentions',
        verbose_name="estudiante"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL, # Si se borra la materia no se pierde, solo se desvincula
        null=True,
        related_name='related_attentions',
        verbose_name="asignatura"
    )

    # --- Campos del Modelo ---
    description = models.TextField(verbose_name="descripción de la consulta")
    channel = models.CharField(
        max_length=20,
        choices=ChannelChoices.choices,
        default=ChannelChoices.IN_PERSON,
        verbose_name="canal de atención"
    )
    attention_date = models.DateTimeField(verbose_name="fecha y hora de la atención")

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        # Devuelve un resumen claro de la atención
        return f"Atención de {self.teacher.username} a {self.student.carnet} el {self.attention_date.strftime('%Y-%m-%d')}"

    class Meta:
        db_table = 'attention'
        verbose_name = 'Atención'
        verbose_name_plural = 'Atenciones'
        ordering = ['-attention_date'] # Ordena de la más reciente a la más antigua
