from rest_framework import generics
from rest_framework.permissions import AllowAny
from rooms.models import Room
from rooms.serializers import RoomListSerializer, RoomDetailSerializer


class RoomListView(generics.ListAPIView):
    """
    Public read-only endpoint returning active rooms.
    Supports ?featured=true query parameter to filter featured rooms.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = RoomListSerializer

    def get_queryset(self):
        queryset = Room.objects.filter(is_active=True).prefetch_related(
            'amenities',
            'images'
        ).order_by('sort_order', 'name')

        featured_param = self.request.query_params.get('featured')
        if featured_param is not None:
            if featured_param.strip().lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(is_featured=True)
            elif featured_param.strip().lower() in ['false', '0', 'no']:
                queryset = queryset.filter(is_featured=False)

        return queryset


class RoomDetailView(generics.RetrieveAPIView):
    """
    Public read-only endpoint returning room details by slug.
    Inactive rooms return HTTP 404.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = RoomDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Room.objects.filter(is_active=True).prefetch_related(
            'amenities',
            'images'
        ).order_by('sort_order', 'name')
