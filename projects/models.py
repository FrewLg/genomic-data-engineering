from django.db import models
from django.contrib.auth.models import User

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
    # submission_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, rel/ated_name="submitted_projects")

    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False) 
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
    # data_entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False,  related_name="entered_samples")
    data_entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False, )
    review_status = models.CharField(
        max_length=50,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        # default="Pending",
         null=True, editable=False
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission {self.submission_id} - {self.project.title}"
