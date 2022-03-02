from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=False, null=True,choices=GENDER_CHOICES, default="")
    email = models.EmailField(unique=True, blank=False, null=True,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    age = models.PositiveIntegerField(blank=False,null=True,
                              error_messages={
                                  'Negative integer': "Please enter a Valid age",
                              })
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=20,
                                    error_messages={
                                        'unique': "A user with that phone number already exists."
                                    })
    medical_history = models.TextField()
    consultation_text = models.TextField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()
