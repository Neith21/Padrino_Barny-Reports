from django.contrib import admin
from .models import Area

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    # --- Vista de Lista ---
    list_display = (
        'name',
        'coordinator__first_name',
        'coordinator__last_name',
        'active',
        'updated_at',
        'modified_by'
    )

    list_filter = ('active', 'coordinator', 'created_at', 'updated_at')
    search_fields = ('name', 'coordinator__username', 'coordinator__first_name', 'coordinator__last_name')
    ordering = ('name',)

    # --- Formulario de Edición/Creación ---
    # Campos que no se podrán editar directamente en el formulario
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'modified_by')
    raw_id_fields = ('coordinator',)

    # Organización del formulario en secciones (fieldsets)
    fieldsets = (
        (None, {
            'fields': ('name', 'coordinator', 'active')
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