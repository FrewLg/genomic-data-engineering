from django.test import TestCase

# Create your tests here.
from decouple import config 
print(config("SECRET_KEY"))