from rest_framework import serializers
from auction.models import Auction_list, Bid



class AuctionListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Auction_list
        fields = ['id', 'title', 'description', 'min_price','deadline']

class BidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ['bidprice']


class MakeBidSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bid
        fields = ['itemid','bidprice']
