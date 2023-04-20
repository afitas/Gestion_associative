
import datetime
from django.db import models
from accounts.models import CustomUser
import datetime


class Subscription(models.Model):
    
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    
    PLAN_CHOICES = (
        ("JANVIER", "janvier"),
        ("FEVRIER", "fevrier"),
        ("MARS", "mars"),
        ("AVRIL", "avril"),
        ("MAI", "mai"),
        ("JUIN", "juin"),
        ("JUILLET", "juillet"),
        ("AOUT", "aout"),
        ("SEPTEMBRE", "septembre"),
        ("OCTOBRE", "octobre"),
        ("NOVEMBRE", "novembre"),
        ("DECEMBRE", "decembre"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.plan } - {self.year}"

    def activate_subscription(self):
        self.is_active = True
        self.end_date = self.start_date.replace(month=self.start_date.month + 11, day=31)
        self.save()

    def deactivate_subscription(self):
        self.is_active = False
        self.end_date = self.start_date.replace(month=self.start_date.month - 1, day=31)
        self.save()

    def get_next_billing_date(self):
        next_billing_date = self.start_date.replace(day=1)
        if self.is_active:
            next_billing_date = self.end_date.replace(day=1) + datetime.timedelta(days=1)
        return next_billing_date

class Fee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.plan} - {self.subscription.year} - {self.date} - {self.amount}"