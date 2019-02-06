from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='USA')
    state = models.CharField(max_length=120)
    postcode = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)
    
    def get_address(self):
        return f'{self.address_line_1} {self.address_line_2 or ""} {self.city} {self.state}, {self.postcode}\n{self.country}'