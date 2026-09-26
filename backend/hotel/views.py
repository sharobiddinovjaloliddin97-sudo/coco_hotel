from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from hotel.models import HotelInformation, Service, GalleryImage, Promotion
from hotel.serializers import (
    HotelInformationSerializer,
    ServiceSerializer,
    GalleryImageSerializer,
    PromotionListSerializer,
    PromotionDetailSerializer,
)


class HotelInformationView(APIView):
    """
    Public read-only endpoint returning current hotel information.
    Gracefully returns fallback data if no record has been created yet.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        instance = HotelInformation.objects.first()
        if not instance:
            return Response(
                {
                    "name": "Coco Hotel",
                    "hero_image": None,
                    "about_image": None,
                    "hero_title": "Welcome to Coco Hotel",
                    "hero_subtitle": "",
                    "about_title": "About Coco Hotel",
                    "about_text": "",
                    "phone": "",
                    "secondary_phone": "",
                    "email": "",
                    "address": "",
                    "map_url": "",
                    "latitude": None,
                    "longitude": None,
                    "check_in_time": None,
                    "check_out_time": None,
                },
                status=status.HTTP_200_OK,
            )
        serializer = HotelInformationSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceListView(generics.ListAPIView):
    """
    Public read-only endpoint returning active hotel services.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(is_active=True).order_by('sort_order', 'name')


class GalleryImageListView(generics.ListAPIView):
    """
    Public read-only endpoint returning active gallery images.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = GalleryImageSerializer

    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True).order_by('sort_order', 'id')


def get_active_promotions_queryset():
    """
    Returns promotions that are active and currently within their valid date window.
    """
    today = timezone.localdate()
    return Promotion.objects.filter(is_active=True).filter(
        Q(valid_from__isnull=True) | Q(valid_from__lte=today)
    ).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=today)
    )


class PromotionListView(generics.ListAPIView):
    """
    Public read-only endpoint returning currently active promotions within date validity.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = PromotionListSerializer

    def get_queryset(self):
        return get_active_promotions_queryset().order_by('sort_order', 'id')


class PromotionDetailView(generics.RetrieveAPIView):
    """
    Public read-only endpoint returning promotion detail by slug.
    Inactive, expired, or future-dated promotions return HTTP 404.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = PromotionDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return get_active_promotions_queryset()
