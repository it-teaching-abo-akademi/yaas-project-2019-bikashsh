from django.db import models
from django.utils import timezone

class Auction_list(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    min_price = models.FloatField(max_length=200)
    deadline = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title