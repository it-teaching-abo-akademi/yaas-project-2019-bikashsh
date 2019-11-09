from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Auction_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auction", null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    min_price = models.FloatField(max_length=200)
    deadline = models.DateTimeField(default=(timezone.now() + timezone.timedelta(hours=72)))

    def __str__(self):
        return self.title
