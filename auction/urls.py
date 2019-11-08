from django.urls import path, re_path
from . import views
from user import views as v


app_name = 'auction'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('user_page/', views.user_page, name='user_page'),
    path('create/', views.CreateAuction.as_view(), name='create'),
    re_path(r'^edit/(?P<id>\d+)/$', views.EditAuction.as_view(), name='edit'),
    re_path(r'^bid/(\d+)/$', views.bid, name='bid'),
    re_path(r'^ban/(\d+)$', views.ban, name='ban'),
    path('resolve/', views.resolve, name='resolve'),
]
