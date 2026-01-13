from django.urls import path
from .views import project_list, project_detail 
from . import views

urlpatterns = [
    path("sss", views.index, name="index"),
    
    path("projects-list/", project_list, name="project_list"),
    path("projects-list/<int:pk>/", project_detail, name="project_detail"),

]



 