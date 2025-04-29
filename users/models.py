from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class CustomerProfile(models.Model):
    user           = models.OneToOneField(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE,
                                        related_name='profile')
    phone_number   = models.CharField(max_length=20, blank=True)
    date_of_birth  = models.DateField(null=True, blank=True)
    # … ander PII-velden …

    def __str__(self):
        return self.user.username


class Address(models.Model):
    profile        = models.ForeignKey(CustomerProfile,
                                       on_delete=models.CASCADE,
                                       related_name='addresses')
    label          = models.CharField(max_length=30,
                                      help_text="e.g. 'Home', 'Work'")
    street         = models.CharField(max_length=100)
    number         = models.CharField(max_length=10)
    zipcode        = models.CharField(max_length=10)
    city           = models.CharField(max_length=50)
    country        = models.CharField(max_length=50)
    is_billing     = models.BooleanField(default=False)
    is_shipping    = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Address"            
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.label} address for {self.profile.user.username}"


