from django.urls import path
from .views import project_list, project_detail , upload_sequence
# from .views import ProjectListView
urlpatterns = [
    # path("sss", views.index, name="index"),
    path("upload/", upload_sequence, name="upload_sequence"),
    path("all/", project_list, name="project_list"),
    path("all/<int:pk>/", project_detail, name="project_detail"),
    # path("projectss/", ProjectListView.as_view(), name="project-list"),

]



 