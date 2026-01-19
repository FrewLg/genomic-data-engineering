from django import forms  # <--- ADD THIS LINE
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from .models import Project
from .forms import ProjectForm ,SampleFormSet
 
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin

FORMS = [
    ("project", ProjectForm),
    ("samples", SampleFormSet),
    ("confirmation", forms.Form), # Empty form just for the confirm step
]

TEMPLATES = {
    "project": "wizard/project_step.html",
    "samples": "wizard/samples_step.html",
    "confirmation": "wizard/confirm_step.html",
}

class ProjectWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
            # 1. Save the Project (Step 1)
            project_form = form_list[0]
            project_instance = project_form.save()

            # 2. Save the Samples (Step 2)
            sample_formset = form_list[1]
            samples = sample_formset.save(commit=False)
            for sample in samples:
                sample.project = project_instance
                sample.save()
            
            sample_formset.save_m2m()

            # 3. Redirect to the detail view of the NEW project
            # 'project_detail' is the name from your urls.py
            # 'pk' is the primary key of the project we just saved
            return redirect('project_detail', pk=project_instance.pk)
# //
class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_lists.html"
    context_object_name = "projects"
    paginate_by = 20  # optional

    def get_queryset(self):
        qs = super().get_queryset().annotate(sample_count=Count("samples"))
        # Search
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(organization__icontains=search) | qs.filter(irb_code__icontains=search)
        return qs.order_by("created_date")

def homepage(request): 
    return render(request, "homepage/homepage.html")

def project_list(request): 
    projects = Project.objects.annotate(sample_count=Count("samples")) 
    return render(request, "projects/project_lists.html",  {
         "projects": projects 
         })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    samples = project.samples.all()  # thanks to related_name
    return render(request, "projects/project_detail.html", {
        "project": project,
        "samples": samples,
    })

def upload_sequence(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = ProjectForm()
    return render(request, "upload.html", {"form": form})

#{"admin": "r00tmepcKV8MwbCT8PdPWu"}
 