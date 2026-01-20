"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from projects.views import homepage , ProjectListView  
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from django.shortcuts import redirect 
def logout_get(request): 
    logout(request) 
    return redirect('home')

urlpatterns = [
path("genome/", admin.site.urls), 

path("all-projects/", ProjectListView.as_view(), name="project-list"),
path("", homepage, name="homepage"), 
path("genomic/", include("projects.urls")),  
path("accounts/", include("allauth.urls")), 
path('projects/', include('projects.urls')),  
path('accounts/', include('allauth.urls')),
 path("login/", LoginView.as_view(template_name="login.html"), name="login"), 
 path("logout/", LogoutView.as_view(next_page="homepage"), name="logout"), 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 