from django.contrib import admin
from .models import Attention

from import_export.admin import ImportExportModelAdmin # 1. Importar
from attention.resources import AttentionResource

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

@admin.register(Attention)
class AttentionAdmin(ImportExportModelAdmin):
    resource_class = AttentionResource

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

    actions = ['export_as_pdf']

    @admin.action(description='Exportar seleccionados a PDF')
    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="atenciones.pdf"'

        # Configuración del documento PDF
        doc = SimpleDocTemplate(response, rightMargin=inch/4, leftMargin=inch/4, topMargin=inch/2, bottomMargin=inch/4)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        elements.append(Paragraph("Reporte de Atenciones", styles['h1']))

        # Preparar los datos para la tabla
        data = [
            ['Fecha', 'Docente', 'Carnet', 'Estudiante', 'Asignatura', 'Canal']
        ]
        for attention in queryset.order_by('attention_date'):
            student_name = f"{attention.student.first_name} {attention.student.last_name}" if attention.student else "N/A"
            data.append([
                attention.attention_date.strftime('%Y-%m-%d %H:%M'),
                attention.teacher.username if attention.teacher else "N/A",
                attention.student.carnet if attention.student else "N/A",
                student_name,
                attention.subject.name if attention.subject else "N/A",
                attention.get_channel_display()
            ])

        # Crear y estilizar la tabla
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        elements.append(table)
        doc.build(elements)

        return response
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(teacher=request.user)

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