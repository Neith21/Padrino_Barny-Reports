from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # --- Vista de Lista ---
    list_display = (
        'carnet',
        'first_name',
        'last_name',
        'career',
        'active'
    )

    list_filter = ('active', 'career', 'created_at', 'updated_at')
    search_fields = ('carnet', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name')

    # --- Formulario de Edición/Creación ---
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    raw_id_fields = ('career',)

    fieldsets = (
        ('Información Personal', {
            'fields': ('carnet', 'first_name', 'last_name', 'email')
        }),
        ('Información Académica', {
            'fields': ('career', 'active')
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