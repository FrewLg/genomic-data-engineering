# check site and social apps
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount
from allauth.account.models import EmailAddress

print("SITE_ID:", settings.SITE_ID)
print("Sites:", list(Site.objects.all().values('id','domain')))
for sa in SocialApp.objects.all():
    print(sa.provider, sa.name, "sites:", list(sa.sites.values_list('id', flat=True)))

# check social accounts and stored emails
for sa in SocialAccount.objects.filter(provider='google'):
    print(sa.user_id, sa.extra_data.get('email'), sa.extra_data.get('verified_email'))
print("EmailAddress entries:", list(EmailAddress.objects.filter(user__socialaccount__provider='google').values('email','verified')))
