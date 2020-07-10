from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.urls import reverse


class UserManager(BaseUserManager):

    def activetion_toggle(self, status, pk=None):
        status = bool(status)
        if pk:
            qs = self.all_users().filter(pk=pk)
            if qs.exists() and qs.count() == 1:
                updated_qs = qs.update(is_active=status)
            else:
                raise Http404

        else:
            updated_qs = self.all_users().update(is_active=status)
        return status

    def all_users(self):
        return self.get_queryset().exclude(is_admin=True)

    def create_user(self, phone_number, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
            is_active=True

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, email, password=None):
        user = self.create_user(
            phone_number,
            username,
            email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        max_length=255,
        unique=True,

    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("accounts:profile_edit", kwargs={"pk": self.pk})

    @property
    def is_staff(self):
        return self.is_admin
