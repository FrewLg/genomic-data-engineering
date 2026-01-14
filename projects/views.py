from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Count
from .models import Project
from .forms import ProjectForm
 
# class ProjectListView(ListView):
#     model = Project
#     template_name = "projects/project_list.html"
#     context_object_name = "projects"
#     paginate_by = 20  # optional

# def get_queryset(self): 
#     qs = super().get_queryset().annotate(sample_count=Count("samples"))  
#     search = self.request.GET.get("q") 
#     if search: 
#         qs = qs.filter(title__icontains=search) | qs.filter(organization__icontains=search) | qs.filter(irb_code__icontains=search) 
#         return qs.order_by("created_date")

 

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
