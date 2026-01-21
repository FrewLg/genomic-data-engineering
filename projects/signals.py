from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver

@receiver(user_signed_up)
def add_user_to_researchers_group_on_signup(request, user, **kwargs):
    researchers_group,  = Group.objects.get_or_create(name="Researchers")
    user.groups.add(researchers_group)

@receiver(user_logged_in)
def add_user_to_researchers_group_on_login(request, user, **kwargs):
    researchers_group,  = Group.objects.get_or_create(name="Researchers")
    user.groups.add(researchers_group)

from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


def assign_researchers_group_on_signup(request, user, **kwargs):
    # Create or get the Researchers group
    researchers_group, _ = Group.objects.get_or_create(name="Researchers")
    # Add the user to the group
    user.groups.add(researchers_group)
    # Do NOT set is_staff here
    user.save()
