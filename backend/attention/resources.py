# tu_app/resources.py

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Attention, Student, Subject
from django.contrib.auth import get_user_model

User = get_user_model()

class AttentionResource(resources.ModelResource):
    # --- Widgets para manejar las ForeignKey ---
    # Le decimos a la librería que al importar/exportar el campo 'teacher',
    # debe buscar al usuario por su 'username'.
    teacher = fields.Field(
        column_name='teacher',
        attribute='teacher',
        widget=ForeignKeyWidget(User, 'username'))

    # Para 'student', usamos su 'carnet' que es un identificador único y amigable.
    student = fields.Field(
        column_name='student',
        attribute='student',
        widget=ForeignKeyWidget(Student, 'carnet'))

    # Para 'subject', usamos su 'name'.
    subject = fields.Field(
        column_name='subject',
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'name'))

    class Meta:
        model = Attention
        fields = ('id', 'teacher', 'student', 'subject', 'attention_date', 'channel', 'description')