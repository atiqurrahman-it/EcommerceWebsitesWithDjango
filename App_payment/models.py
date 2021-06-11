from django.db import models
from django.conf import settings


# Create your models here.


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=55, blank=True)
    country = models.CharField(max_length=65, blank=True)

    def __str__(self):
        return f'{self.user.profile.username} Billing Address'  # profile import user_login App  profile model

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value == '':
                return False
        return True

    class Meta:
        verbose_name_plural = "Billing Addresses"
