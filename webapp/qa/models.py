from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractUser):
    department = models.ManyToManyField(Department, blank=False)
    is_boss = models.BooleanField(default=False)


class Document(models.Model):
    title = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documents')
    allowed_departments = models.ManyToManyField(Department, blank=True, related_name='documents')
    visible_to = models.ManyToManyField(User, blank=True, related_name='visible_documents')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title