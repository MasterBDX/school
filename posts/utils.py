import random
import string
import os
from django.utils.text import slugify
from . import models


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = random_string_generator(size=8)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{randstr}".format(
            randstr=random_string_generator(size=10)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_key_generator(class_, new_key=None):
    size = random.randint(35, 45)
    if new_key is not None:
        key = new_key
    else:
        key = random_string_generator(size=size)

    qs_exists = class_.objects.filter(key__iexact=key).exists()
    if qs_exists:
        new_key = "{randstr}".format(
            randstr=random_string_generator(size=45)
        )
        return unique_key_generator(instance, new_key=new_key)
    return key
