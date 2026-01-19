# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Project, SamplesMetadata

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'duration', 'organization', 'description','attachment' ]

class SampleForm(forms.ModelForm):
    class Meta:
        model = SamplesMetadata
        fields = ['sample_type', 'organism', 'host', 'phenotype', 'facility_lab','referring_lab','location',
                  'sequencing',
                  ]

# Create the formset for the "Many" part
SampleFormSet = inlineformset_factory(
    Project, SamplesMetadata, form=SampleForm, 
    extra=1, can_delete=True
)
