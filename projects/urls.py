from django.urls import path
from .views import project_list, project_detail , upload_sequence
from .views import ProjectWizard, FORMS

urlpatterns = [
    path("upload/", upload_sequence, name="upload_sequence"),
    path("all/", project_list, name="project_list"),
    path("all/<int:pk>/", project_detail, name="project_detail"),
    path('create-project/', ProjectWizard.as_view(FORMS), name='project_wizard'),
    path('wizard/', ProjectWizard.as_view(FORMS), name='project_wizard'),
]



 