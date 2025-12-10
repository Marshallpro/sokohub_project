
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer',null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sokohub_user_groups', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sokohub_user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"