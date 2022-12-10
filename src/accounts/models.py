from django.contrib.auth.models import AbstractUser
from django.db import models
from cocognite import settings


class User(AbstractUser):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )

    is_customer = models.BooleanField(default=True, help_text="This account belongs to customer")
    profile_image = models.ImageField(
        null=True, blank=True,
        upload_to='images/profiles/',
        verbose_name="Profile Picture", help_text="Profile image must be 150*150 in size of png, jpg or jpeg"
    )
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE)
    about = models.TextField(null=True, blank=True, help_text="Tell us something interesting about yourself")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    donations_total = models.PositiveIntegerField(default=0)
    donations_amount = models.FloatField(default=0)
    donations_projects = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)
