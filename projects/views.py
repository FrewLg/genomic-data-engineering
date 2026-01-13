from django.shortcuts import render, redirect, get_object_or_404
 
from .forms import ProjectForm

def homepage(request): 
    return render(request, "homepage/homepage.html")

def project_list(request): 
    projects = Project.objects.all() 
    return render(request, "projects/project_list.html", {
        "projects": projects
        
        })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    samples = project.samples.all()  # thanks to related_name
    return render(request, "projects/project_detail.html", {
        "project": project,
        "samples": samples,
    })
# def upload_sequence(request): if request.method == "POST": form = ProjectForm(request.POST, request.FILES) if form.is_valid(): form.save() return redirect("success_page") # replace with your success view else: form = ProjectForm() return render(request, "upload.html", {"form": form})

def upload_sequence(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = ProjectForm()
    return render(request, "upload.html", {"form": form})
