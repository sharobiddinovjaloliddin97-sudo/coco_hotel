from rest_framework import serializers
from core.language import get_request_language, resolve_multilingual_value
from rooms.models import Amenity, Room, RoomImage


class AmenitySerializer(serializers.ModelSerializer):
    """
    Public serializer for room amenities with localized name.
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon']

    def get_name(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'name', lang)


class RoomImageSerializer(serializers.ModelSerializer):
    """
    Public serializer for room gallery and primary images.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'sort_order']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class RoomListSerializer(serializers.ModelSerializer):
    """
    Concise public serializer for room catalogue listings with localized fields.
    """
    amenities = AmenitySerializer(many=True, read_only=True)
    primary_image = RoomImageSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    bed_type = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'price_per_night',
            'max_adults',
            'max_children',
            'bed_type',
            'room_size',
            'is_featured',
            'amenities',
            'primary_image',
        ]

    def get_name(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'name', lang)

    def get_short_description(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'short_description', lang)

    def get_bed_type(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'bed_type', lang)


class RoomDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive public serializer for room detail view with localized fields.
    """
    amenities = AmenitySerializer(many=True, read_only=True)
    images = RoomImageSerializer(many=True, read_only=True)
    primary_image = RoomImageSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    bed_type = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'description',
            'price_per_night',
            'max_adults',
            'max_children',
            'bed_type',
            'room_size',
            'is_featured',
            'amenities',
            'primary_image',
            'images',
            'created_at',
            'updated_at',
        ]

    def get_name(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'name', lang)

    def get_short_description(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'short_description', lang)

    def get_description(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'description', lang)

    def get_bed_type(self, obj):
        request = self.context.get('request')
        lang = get_request_language(request)
        return resolve_multilingual_value(obj, 'bed_type', lang)
