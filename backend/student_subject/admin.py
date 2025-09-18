from django.contrib import admin
from .models import StudentSubject

@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    # --- Vista de Lista ---
    list_display = (
        'student',
        'subject',
        'active',
        'created_at'
    )

    list_filter = ('active', 'subject', 'created_at', 'updated_at')

    search_fields = (
        'student__carnet',
        'student__first_name',
        'student__last_name',
        'subject__name',
        'subject__section'
    )

    ordering = ('student__last_name', 'student__first_name', 'subject__name')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    raw_id_fields = ('student', 'subject')

    fieldsets = (
        ('Inscripción', {
            'fields': ('student', 'subject', 'active')
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
