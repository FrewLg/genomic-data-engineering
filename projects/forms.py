# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Project, SamplesMetadata

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'duration', 'organization', 'description','duration', 'mou', 'attachment','metadata_type','irb_code' ]

# class SampleForm(forms.ModelForm):
#     class Meta:
#         model = SamplesMetadata
    
#         fields = [
#             'sample_type', 'organism', 'host', 'phenotype', 'facility_lab', 'referring_lab', 'location',
#             'sequencing',
#             'parasite_density', 'life_stage', 'propagation', 'drug_exposure_history',
#             'serotype_or_lineage', 'serotype', 'strain', 'isolate', 'viral_load', 'ct_value', 'phenotype_notes',
#         ]
class SampleForm(forms.ModelForm):
    class Meta:
        model = SamplesMetadata
        fields = [
            'sample_type', 'organism', 'host', 'phenotype', 'facility_lab', 'referring_lab', 'location',
            'sequencing',
            'parasite_density', 'life_stage', 'propagation', 'drug_exposure_history',
            'serotype_or_lineage', 'serotype', 'strain', 'isolate', 'viral_load', 'ct_value', 'phenotype_notes',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # widgets = { "name": forms.TextInput(attrs={"class": "form-control"}), "description": forms.Textarea(attrs={"class": "form-control"}), }

SampleFormSet = inlineformset_factory(
    Project, SamplesMetadata, form=SampleForm, 
    extra=1, 
    can_delete=False
)

 