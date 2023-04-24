
import datetime
from django.db import models
from accounts.models import CustomUser



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

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    

    def __str__(self):
        return f"{self.plan } - {self.year}"


class Fee(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.subscription.plan} - {self.subscription.year} - {self.date} - {self.amount}"