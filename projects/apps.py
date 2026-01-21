from django.apps import AppConfig

# from django.apps import AppConfig
class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'
    def ready(self): 
        import projects.signals 
        # ensures signals are loaded
class PhenotypeMetadataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PhenotypeMetadata'

class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"



 
 