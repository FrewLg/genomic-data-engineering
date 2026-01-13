from django.http import HttpResponse
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Project

def index():

    return HttpResponse("Hello, world. You're at the poddlls index.")



def project_list(request): 
    projects = Project.objects.all() 
    return render(request, "projects/project_list.html", {"projects": projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    samples = project.samples.all()  # thanks to related_name
    return render(request, "projects/project_detail.html", {
        "project": project,
        "samples": samples,
    })
