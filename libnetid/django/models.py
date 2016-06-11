from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.conf import settings


class LibNetidUserManager(UserManager):
    def _create_user(self, netid, password, **extra_fields):
        user = self.model(netid=netid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, netid, password=None, **extra_fields):
        return self._create_user(netid, password, **extra_fields)

    def create_superuser(self, netid, email, password, **extra_fields):
        return self._create_user(netid, email, password, is_staff=True, **extra_fields)


class AbstractNetidUser(AbstractBaseUser):
    # Fields given by ULB api
    netid = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    raw_matricule = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(blank=True, default=datetime.date(1970, 1, 1))
    library = models.CharField(max_length=255, blank=True)

    # Mandatory Django fields
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = []
    objects = LibNetidUserManager()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.netid

    # Convenience methods and properties.

    @property
    def matricule(self):
        return self.raw_matricule.split(':')[-1]

    class Meta:
        abstract = True


class Inscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    faculty = models.CharField(max_length=80, blank=True, default='')
    section = models.CharField(max_length=80, blank=True, default='')
    year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'section', 'faculty', 'year')
