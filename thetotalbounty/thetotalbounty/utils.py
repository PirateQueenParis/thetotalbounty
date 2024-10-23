
from django.utils.crypto import get_random_string


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + '-' + get_random_string(length=4)
    return unique_slug


def get_user_display_name(user, profiles):
    validProfiles = profiles.filter(user=user)
    if validProfiles.count() > 0:
        return validProfiles[0].display_name
    else:
        return user
