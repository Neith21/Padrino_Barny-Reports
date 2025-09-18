from django.contrib import admin
from .models import Attention

@admin.register(Attention)
class AttentionAdmin(admin.ModelAdmin):
    # --- Vista de Lista ---
    list_display = (
        'attention_date',
        'teacher',
        'get_student_carnet', # Usamos un método personalizado para el carnet
        'student',
        'subject',
        'channel',
    )

    list_filter = ('attention_date', 'channel', 'teacher', 'subject')

    search_fields = (
        'student__carnet',
        'student__first_name',
        'student__last_name',
        'teacher__username',
        'teacher__first_name',
        'subject__name',
        'description'
    )
    ordering = ('-attention_date',)

    # --- Formulario de Edición/Creación ---
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    raw_id_fields = ('teacher', 'student', 'subject')
    autocomplete_fields = ('teacher', 'student', 'subject')

    fieldsets = (
        ('Registro de Atención', {
            'fields': (
                'teacher', 
                'student', 
                'subject', 
                'attention_date', 
                'channel', 
                'description'
            )
        }),
        ('Información de Auditoría', {
            'classes': ('collapse',),
            'fields': ('created_by', 'created_at', 'modified_by', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Carnet Estudiante', ordering='student__carnet')
    def get_student_carnet(self, obj):
        """
        Método personalizado para mostrar el carnet del estudiante en la lista.
        """
        if obj.student:
            return obj.student.carnet
        return "N/A"