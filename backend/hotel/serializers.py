from rest_framework import serializers
from core.language import get_request_language, resolve_multilingual_value
from hotel.models import HotelInformation, Service, GalleryImage, Promotion


class HotelInformationSerializer(serializers.ModelSerializer):
    """
    Public serializer for hotel details, branding, contact and location with localized content.
    """
    hero_title = serializers.SerializerMethodField()
    hero_subtitle = serializers.SerializerMethodField()
    about_title = serializers.SerializerMethodField()
    about_text = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = HotelInformation
        fields = [
            'name',
            'hero_image',
            'about_image',
            'hero_title',
            'hero_subtitle',
            'about_title',
            'about_text',
            'phone',
            'secondary_phone',
            'email',
            'address',
            'map_url',
            'latitude',
            'longitude',
            'check_in_time',
            'check_out_time',
        ]

    def get_hero_title(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'hero_title', lang)

    def get_hero_subtitle(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'hero_subtitle', lang)

    def get_about_title(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'about_title', lang)

    def get_about_text(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'about_text', lang)

    def get_address(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'address', lang)


class ServiceSerializer(serializers.ModelSerializer):
    """
    Public serializer for hotel services with localized name and description.
    """
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'icon', 'sort_order']

    def get_name(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'name', lang)

    def get_description(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'description', lang)


class GalleryImageSerializer(serializers.ModelSerializer):
    """
    Public serializer for gallery showcase images with localized title and alt_text.
    """
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    alt_text = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'title', 'alt_text', 'sort_order', 'category']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_title(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'title', lang)

    def get_alt_text(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'alt_text', lang)


class PromotionListSerializer(serializers.ModelSerializer):
    """
    Public list serializer for special offers and promotions with localized title and summary.
    """
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'image',
            'valid_from',
            'valid_until',
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_title(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'title', lang)

    def get_short_description(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'short_description', lang)


class PromotionDetailSerializer(serializers.ModelSerializer):
    """
    Public detail serializer for promotion view with localized title, summary, and details.
    """
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'description',
            'image',
            'valid_from',
            'valid_until',
            'created_at',
            'updated_at',
        ]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_title(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'title', lang)

    def get_short_description(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'short_description', lang)

    def get_description(self, obj):
        lang = get_request_language(self.context.get('request'))
        return resolve_multilingual_value(obj, 'description', lang)
