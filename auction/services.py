from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from auction.models import Auction_list, Bid
from auction.serializers import AuctionListSerializer, BidSerializer,MakeBidSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes
import decimal


class BrowseAuctionApi(APIView):
    def get(self,request,format=None):
    	auction=Auction_list.objects.filter(state="A")
    	searializer=AuctionListSerializer(auction,many=True)
    	return Response(searializer.data)


class SearchAuctionApi(APIView):
	def get(self,request,title,format=None):
		auction=Auction_list.objects.filter(title=title)
		searializer=AuctionListSerializer(auction,many=True)
		return Response(searializer.data)


class SearchAuctionWithTermApi(APIView):
	def get(self,request,format=None):
		title=self.request.query_params.get("term","")
		auction=Auction_list.objects.filter(title=title)
		searializer=AuctionListSerializer(auction,many=True)
		return Response(searializer.data)


class SearchAuctionApiById(APIView):
	def get(self,request,id,format=None):
		auction=Auction_list.objects.filter(id=id)
		searializer=AuctionListSerializer(auction,many=True)
		return Response(searializer.data)

@permission_classes((permissions.IsAuthenticated,))
class BidAuctionApi(APIView):
	def post(self,request,id,format=None):
		bid=Bid.objects.get(itemid=id)
		searializer=MakeBidSerializer(bid,data=request.data)
		auction = Auction_list.objects.get(id =id)

		print(auction)
		if not (auction.state =="A"):
			content={"messages": "Sorry, The bid is not active"}
			return Response(content)
		if(request.user.username==auction.user.username):
			content={"messages": "Sorry, You can not bid in your bid"}
			return Response(content)
		else:
			new_price=decimal.Decimal(request.data)
			old_price=bid.bidprice
			if(new_price>old_price):
				bid.bidprice=new_price
				bid.user=request.user
				bid.save()
				content={ "message" : "Bid successfully",
						"title": auction.title,
						"description":auction.description,
						"current_price": bid.bidprice,
						"deadline_date": auction.deadline}
			else:
				content={"messages": "Sorry, Your bid is not higher then winning bid"}

			return Response(content)
	def get(self,request,id,format=None):
		bid=Bid.objects.filter(itemid=id)
		searializer=BidSerializer(bid,many=True)
		return Response(searializer.data)