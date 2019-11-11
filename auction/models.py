from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Auction_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auction", null=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    min_price = models.FloatField(max_length=200)
    deadline = models.DateTimeField(default=(timezone.now() + timezone.timedelta(hours=72)))
    state = models.CharField(max_length=1, default="A")

    def __str__(self):
        return self.title

class Bid(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	itemid=models.ForeignKey(Auction_list,on_delete=models.CASCADE)
	bidprice=models.DecimalField(max_digits=10, decimal_places=2)

class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language_pref = models.CharField(max_length=5, null=True)