from django.urls import path
from hotel.views import (
    HotelInformationView,
    ServiceListView,
    GalleryImageListView,
    PromotionListView,
    PromotionDetailView,
)

app_name = 'hotel'

urlpatterns = [
    path('hotel/', HotelInformationView.as_view(), name='hotel-info'),
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('gallery/', GalleryImageListView.as_view(), name='gallery-list'),
    path('promotions/', PromotionListView.as_view(), name='promotion-list'),
    path('promotions/<slug:slug>/', PromotionDetailView.as_view(), name='promotion-detail'),
]
