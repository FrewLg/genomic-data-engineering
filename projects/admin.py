from django.contrib import admin
 
# from .models import Project, ProjectStatus, MetadataType
from .models import (
    Project, 
    ProjectStatus,
    MetadataType,
    SamplesMetadata,
    LabFacility,
    Organism,
    SampleType,
    Location,
    HostMetadata,
    SequencingMetadata,
    PhenotypeMetadata,
)

 

admin.site.site_header = "EPHI- GenDE "
admin.site.site_title = "Admin"
admin.site.index_title = "Management Dashboard"
# Injecting CSS globally
admin.autodiscover()
admin.site.enable_nav_sidebar = True # Optional

# Add the media property to the global site object
admin.site.index_template = None
#TabularInline vs StackedInline
class SamplesMetadataInline(admin.StackedInline):
    model = SamplesMetadata
    extra = 1  # number of empty forms shown by default


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_id", "title", "attachment", "organization", "status", "submitted_by",   "submission_date",  )
    search_fields = ("title", "organization", "irb_code")
    # list_filter = ("status", "submission_date",  )
    ordering = ("created_date",)
    inlines = [SamplesMetadataInline]


@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }

@admin.register(MetadataType)
class MetadataTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

 

@admin.register(SamplesMetadata)
class SamplesMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "submission_id",
        "project",
        # "user",
        "facility_lab",
        "referring_lab",
        "organism",
        "sample_type",
        "location",
        "host",
        "sequencing",
        "phenotype",
        # "entry_date",
        # "data_entered_by",
        "review_status",
    )
    search_fields = ("submission_id", "project__title", "user__username", "organism__name")
    list_filter = ("review_status", "entry_date", "facility_lab", "organism", "sample_type")
    ordering = ("-entry_date",)
    # exclude= ("user",   )
# Or group them into sections 
    fieldsets = ( 
        ("Project --", {"fields": ("project",   "entry_date",  ),
                        "classes": ("wide",),  }),
        ("Sample Details", { "fields": ("organism", "sample_type", "location", "host"), "classes": ("wide",), }), 
        ("Lab Details", { "fields": ("facility_lab", "referring_lab", "sequencing", "phenotype") ,"classes": ("wide",),}), 
        ("Review", { "fields": ( ) }), )
    def save_model(self, request, obj, form, change): 
        if not obj.pk: # only set on creation 
            obj.data_entered_by = request.user 
            super().save_model(request, obj, form, change)
    def get_user(self, obj): 
        return obj.user.username # or obj.user.email 
    # get_user.admin_order_field = "user" # allows sorting 
    # get_user.short_description = "Submitted By"
@admin.register(LabFacility)
class LabFacilityAdmin(admin.ModelAdmin):
    list_display = ("lab_id", "name")
    search_fields = ("name",)


@admin.register(Organism)
class OrganismAdmin(admin.ModelAdmin):
    list_display = ("organism_id", "name")
    search_fields = ("name",)


@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    list_display = ("sample_type_id", "type_name")
    search_fields = ("type_name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("location_id", "name")
    search_fields = ("name",)


@admin.register(HostMetadata)
class HostMetadataAdmin(admin.ModelAdmin):
    list_display = ("host_id", "host_name")
    search_fields = ("host_name",)


@admin.register(SequencingMetadata)
class SequencingMetadataAdmin(admin.ModelAdmin):
    list_display = ("sequencing_id", "platform")
    search_fields = ("platform",)
    exclude = ("review_status", "remarks")

@admin.register(PhenotypeMetadata)
class PhenotypeMetadataAdmin(admin.ModelAdmin):
    list_display = ("phenotype_id", "description")
    search_fields = ("description",)


# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [SamplesMetadataInline]
