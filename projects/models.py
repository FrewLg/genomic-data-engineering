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
    submission_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_projects")
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE)

    attachment = models.CharField(max_length=255, null=True, blank=True)
    mou = models.CharField(max_length=255, null=True, blank=True)

    organization = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)

    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_projects")
    metadata_type = models.ForeignKey(MetadataType, on_delete=models.SET_NULL, null=True, blank=True)

    irb_code = models.CharField(max_length=255, null=True, blank=True)
    approved_at = models.DateField(null=True, blank=True)
    sample_submitted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
