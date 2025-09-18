from django.conf import settings
from django.db import models
from student.models import Student
from subject.models import Subject

class StudentSubject(models.Model):
    # --- Relaciones ---
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE, # Si se borra el estudiante, se borra esta inscripción
        related_name='subjects_taken',
        verbose_name="estudiante"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE, # Si se borra la materia, se borra esta inscripción
        related_name='enrolled_students',
        verbose_name="asignatura"
    )

    # --- Campos de Auditoría ---
    active = models.BooleanField(default=True, verbose_name="activo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="modificado por")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="última modificación")

    def __str__(self):
        # Devuelve una representación clara de la relación
        return f"{self.student.first_name} {self.student.last_name} -> {self.subject.name}"

    class Meta:
        db_table = 'student_subject'
        verbose_name = 'Inscripción de Estudiante en Asignatura'
        verbose_name_plural = 'Inscripciones de Estudiantes en Asignaturas'
        # Restricción para que un estudiante no pueda ser inscrito dos veces en la misma materia
        constraints = [
            models.UniqueConstraint(fields=['student', 'subject'], name='unique_student_enrollment')
        ]
        ordering = ['student__last_name', 'subject__name'] # Ordena por apellido de estudiante y luego por materia