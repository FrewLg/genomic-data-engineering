from django.conf import settings  

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

 

class ProjectStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MetadataType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,  
        blank=True
    )
    submission_date = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.ForeignKey(ProjectStatus, on_delete=models.SET_NULL, null=True, editable=False)
    attachment = models.FileField(upload_to="project_attachments/", blank=True, null=True)
    mou = models.FileField(upload_to="project_attachments/", blank=True, null=True)
    sequence_result = models.FileField(upload_to="sequence_result/", blank=True, null=True)
    organization = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name="approved_projects")
    metadata_type = models.ForeignKey(MetadataType, on_delete=models.SET_NULL, null=True, blank=True)
    irb_code = models.CharField(max_length=255, null=True, blank=True)
    approved_at = models.DateField(auto_now_add=True, editable=False)
    sample_submitted_at = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title



class LabFacility(models.Model):
    lab_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Organism(models.Model):
    organism_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SampleType(models.Model):
    sample_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name

class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HostMetadata(models.Model):
    host_id = models.AutoField(primary_key=True)
    host_name = models.CharField(max_length=255)

    def __str__(self):
        return self.host_name


class SequencingMetadata(models.Model):
    sequencing_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=255)

    def __str__(self):
        return self.platform


class PhenotypeMetadata(models.Model):
    phenotype_id = models.AutoField(primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f"Phenotype {self.phenotype_id}"


class SamplesMetadata(models.Model):
    submission_id = models.AutoField(primary_key=True)  # SERIAL PK
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="samples")
    facility_lab = models.ForeignKey(LabFacility, on_delete=models.CASCADE, related_name="facility_samples")
    referring_lab = models.ForeignKey(LabFacility, on_delete=models.CASCADE, related_name="referring_samples")
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    sample_type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    host = models.ForeignKey(HostMetadata, on_delete=models.CASCADE)
    sequencing = models.ForeignKey(SequencingMetadata, on_delete=models.CASCADE)
    phenotype = models.ForeignKey(PhenotypeMetadata, on_delete=models.CASCADE)
    entry_date = models.DateField(null=True, blank=True )  # Default CURRENT_TIMESTAMP
    data_entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, )
    review_status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending",
         null=True, editable=False
    )
    remarks = models.TextField(blank=True, null=True)
    parasite_density = models.FloatField(null=True, blank=True, help_text="Parasites per µL or specified unit")
    life_stage = models.CharField(max_length=50, null=True, blank=True, help_text="e.g., trophozoite, gametocyte")
    propagation = models.CharField(max_length=100, null=True, blank=True, help_text="In vitro, in vivo, clinical")
    drug_exposure_history = models.TextField(null=True, blank=True, help_text="Drugs and exposure timeline")
    serotype_or_lineage = models.CharField(max_length=100, null=True, blank=True, help_text="Combined serotype or lineage")
    serotype = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    strain = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    isolate = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    viral_load = models.FloatField(null=True, blank=True, help_text="Viral copies per mL or specified unit")
    ct_value = models.FloatField(null=True, blank=True, help_text="PCR cycle threshold value")
    phenotype_notes = models.TextField(null=True, blank=True, help_text="Phenotypic observations and notes")

    class Meta:
        indexes = [
            models.Index(fields=['serotype']),
            models.Index(fields=['strain']),
            models.Index(fields=['isolate']),
        ]


    def __str__(self):
        return f"Submission {self.submission_id} - {self.project.title}"

# -----------------------.py

# Import or define lookup models in this module or import them:
# from .lookups import LifeStage, PropagationMethod, Serotype, Lineage, Unit

# class SamplesMetadata(models.Model):
#     submission_id = models.AutoField(primary_key=True)  # SERIAL PK
#     # Existing relationships
#     project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="samples")
#     facility_lab = models.ForeignKey("LabFacility", on_delete=models.CASCADE, related_name="facility_samples")
#     referring_lab = models.ForeignKey("LabFacility", on_delete=models.CASCADE, related_name="referring_samples")
#     organism = models.ForeignKey("Organism", on_delete=models.CASCADE)
#     sample_type = models.ForeignKey("SampleType", on_delete=models.CASCADE)
#     location = models.ForeignKey("Location", on_delete=models.CASCADE )
#     host = models.ForeignKey( "HostMetadata", on_delete=models.CASCADE )
#     sequencing = models.ForeignKey(  "SequencingMetadata", on_delete=models.CASCADE)
#     phenotype = models.ForeignKey("PhenotypeMetadata", on_delete=models.CASCADE)
#     # New quantitative measurements
#     parasite_density = models.DecimalField(max_digits=20, decimal_places=6, validators=[MinValueValidator(0)],blank=True, null=True, help_text="Parasites per unit (see parasite_density_unit)" )
#     parasite_density_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, blank=True, null=True, related_name="parasite_density_samples" )
#     viral_load = models.DecimalField( max_digits=30, decimal_places=6, validators=[MinValueValidator(0)], blank=True, null=True, help_text="Viral load (e.g., copies/mL)" )
#     viral_load_unit = models.ForeignKey( "Unit", on_delete=models.SET_NULL, blank=True, null=True,  related_name="viral_load_samples")
#     ct_value = models.DecimalField( max_digits=6, decimal_places=3, validators=[MinValueValidator(0)], blank=True, null=True, help_text="qPCR cycle threshold value" )
#     # Controlled lookups via foreign tables
#     life_stage = models.ForeignKey( "LifeStage", on_delete=models.SET_NULL, blank=True, null=True, related_name="samples")
#     propagation = models.ForeignKey("PropagationMethod", on_delete=models.SET_NULL, blank=True, null=True, related_name="samples")
#     serotype = models.ForeignKey("Serotype", on_delete=models.SET_NULL, blank=True, null=True, related_name="samples")
#     serotype_or_lineage = models.ForeignKey("Lineage", on_delete=models.SET_NULL, blank=True, null=True, related_name="samples")
#     # Identifiers and strain/isolate
#     strain = models.CharField(max_length=128, blank=True, null=True)
#     isolate = models.CharField(max_length=128, blank=True, null=True, help_text="Local or accession isolate id")
#     # Free text and structured fields
#     phenotype_notes = models.TextField(blank=True, null=True)
#     drug_exposure_history = models.JSONField(blank=True, null=True,help_text="List of drug exposures. Example: [{'drug_name':'chloroquine','dose':'25 mg/kg','start_date':'2025-01-01','end_date':'2025-01-03'}]")
#     # File pointers and assay metadata
#     raw_file_path = models.CharField(max_length=1024, blank=True, null=True, help_text="Object store path for raw file")
#     processed_file_path = models.CharField(max_length=1024, blank=True, null=True, help_text="Object store path for processed artifact")
#     assay_method = models.CharField(max_length=128, blank=True, null=True)
#     assay_protocol_ref = models.CharField(max_length=256, blank=True, null=True)

#     # Consent and governance
#     consent_flags = models.JSONField(blank=True, null=True,help_text="Consent and permitted uses. Example: {'research': True, 'commercial': False, 'retention_until':'2030-01-01'}" )

#     # Audit fields
#     created_at = models.DateTimeField(default=timezone.now, editable=False)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Samples Metadata"
#         verbose_name_plural = "Samples Metadata"
#         indexes = [
#             models.Index(fields=["submission_id"]),
#             models.Index(fields=["project"]),
#             models.Index(fields=["isolate"]),
#             # models.Index(fields=["collection_date"])
#             #  if "collection_date" in [f.name for f in models.get_models()] 
#             # else models.Index(fields=["submission_id"]),
#         ]
#         ordering = ["-created_at"]

#     def __str__(self):
#         if self.isolate:
#             return f"{self.isolate} (submission {self.submission_id})"
#         return f"submission {self.submission_id}"

#     def to_dict(self):
#         return {
#             "submission_id": self.submission_id,
#             "project_id": self.project_id,
#             "facility_lab_id": self.facility_lab_id,
#             "referring_lab_id": self.referring_lab_id,
#             "organism_id": self.organism_id,
#             "sample_type_id": self.sample_type_id,
#             "location_id": self.location_id,
#             "host_id": self.host_id,
#             "sequencing_id": self.sequencing_id,
#             "phenotype_id": self.phenotype_id,
#             "parasite_density": float(self.parasite_density) if self.parasite_density is not None else None,
#             "parasite_density_unit": self.parasite_density_unit_id,
#             "viral_load": float(self.viral_load) if self.viral_load is not None else None,
#             "viral_load_unit": self.viral_load_unit_id,
#             "ct_value": float(self.ct_value) if self.ct_value is not None else None,
#             "life_stage_id": self.life_stage_id,
#             "propagation_id": self.propagation_id,
#             "serotype_id": self.serotype_id,
#             "serotype_or_lineage_id": self.serotype_or_lineage_id,
#             "strain": self.strain,
#             "isolate": self.isolate,
#             "phenotype_notes": self.phenotype_notes,
#             "drug_exposure_history": self.drug_exposure_history,
#             "raw_file_path": self.raw_file_path,
#             "processed_file_path": self.processed_file_path,
#             "assay_method": self.assay_method,
#             "assay_protocol_ref": self.assay_protocol_ref,
#             "consent_flags": self.consent_flags,
#             "created_at": self.created_at.isoformat(),
#             "updated_at": self.updated_at.isoformat(),
#         }


# parasite_density
# life_stage
# propagation
# drug_exposure_history
# serotype_or_lineage
# serotype
# strain
# isolate
# viral_load
# ct_value
# phenotype_notes

