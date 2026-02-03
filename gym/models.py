from django.db import models
from django.utils import timezone  # Make sure this line exists
from datetime import date, timedelta
from django.contrib.auth.models import User

# Inside your Member class
@property
def days_remaining(self):
    if self.expiry_date:
        today = date.today()
        delta = self.expiry_date - today
        return max(0, delta.days)  # Returns 0 if already expired
    return 0
class Plan(models.Model):
    name = models.CharField(max_length=50) # Plan A, B, C
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - ₱{self.price}"

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # Link Member to Plan
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(default=date.today)
    expiry_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def status(self):
        from django.utils import timezone
        return "Active" if self.expiry_date >= timezone.now().date() else "Expired"

    @property
    def days_remaining(self):
        today = date.today()
        delta = self.expiry_date - today
        return max(0, delta.days)
