from django import forms  # <--- ADD THIS LINE
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Project
from .forms import ProjectForm ,SampleFormSet
from django.contrib import messages
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.views import LogoutView
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


# Profile view (only for logged-in users)
@login_required
def profile_view(request):
    return render(request, "homepage/profile.html", {"user": request.user})

# Logout view (you can also use Django’s built-in LogoutView directly in urls.py)
class CustomLogoutView(LogoutView):
    next_page = "home"  # redirect after logout (use your homepage URL name)


class ProjectWizard(LoginRequiredMixin, SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs): 
        # 1. Get the Project Form (Index 0)
        project_form = form_list[0]
        project_instance = project_form.save(commit=False)
        
        # 2. Assign the user to the PROJECT instance
        project_instance.submitted_by = self.request.user
        project_instance.save() # Save project first to get an ID for the samples

        # 3. Get the Sample Formset (Index 1)
        sample_formset = form_list[1]
        samples = sample_formset.save(commit=False)
        
        # 4. Link each sample to the project we just saved
        for sample in samples:
            sample.project = project_instance
            sample.save()
        
        # 5. Finalize many-to-many relationships if any
        sample_formset.save_m2m()
        
        # 6. Success message and redirect
        messages.success(self.request, f"Project '{project_instance.title}' created successfully with {len(samples)} samples.")
        return redirect('project_detail', pk=project_instance.pk)
# //
class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_lists.html"
    context_object_name = "projects"
    paginate_by = 20  # optional
    permission_required = "projects.view_project"
    def get_queryset(self):
        qs = super().get_queryset().annotate(sample_count=Count("samples"))
        # Search
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(organization__icontains=search) | qs.filter(irb_code__icontains=search)
        return qs.order_by("created_date")

def homepage(request): 
    return render(request, "homepage/homepage.html")

@login_required # This ensures the user is logged in before seeing the list
def project_list(request): 
    # projects = Project.objects.annotate(sample_count=Count("samples")) 
    projects = Project.objects.filter(submitted_by=request.user).annotate(
        sample_count=Count("samples")
    )
    return render(request, "projects/project_lists.html",  {
         "projects": projects 
         })
@login_required
@permission_required("projects.view_project", raise_exception=True)
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    samples = project.samples.all()  # thanks to related_name
    return render(request, "projects/project_detail.html", {
        "project": project,
        "samples": samples,
    })
@login_required
def upload_sequence(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = ProjectForm()
    return render(request, "upload.html", {"form": form})

# Airflow {"admin": "r00tmepcKV8MwbCT8PdPWu"}
 