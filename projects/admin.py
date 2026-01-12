from django.contrib import admin
from .models import Project, ProjectStatus, MetadataType

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_id", "title", "organization", "status", "submitted_by", "approved_by", "submission_date", "approved_at")
    search_fields = ("title", "organization", "irb_code")
    list_filter = ("status", "submission_date", "approved_at")
    ordering = ("-created_date",)

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(MetadataType)
class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
