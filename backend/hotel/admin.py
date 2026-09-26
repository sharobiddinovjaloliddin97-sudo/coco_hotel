from django.contrib import admin
from hotel.models import HotelInformation, Service, GalleryImage, Promotion


@admin.register(HotelInformation)
class HotelInformationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'email',
        'address',
        'check_in_time',
        'check_out_time',
        'updated_at'
    )
    fieldsets = (
        ('Shared Settings & Contact', {
            'fields': (
                'name',
                'hero_image',
                'about_image',
                'phone',
                'secondary_phone',
                'email',
                'map_url',
                'latitude',
                'longitude',
                'check_in_time',
                'check_out_time'
            )
        }),
        ('English Content', {
            'fields': (
                'hero_title_en',
                'hero_subtitle_en',
                'about_title_en',
                'about_text_en',
                'address_en'
            )
        }),
        ('Uzbek Content', {
            'fields': (
                'hero_title_uz',
                'hero_subtitle_uz',
                'about_title_uz',
                'about_text_uz',
                'address_uz'
            )
        }),
        ('Russian Content', {
            'fields': (
                'hero_title_ru',
                'hero_subtitle_ru',
                'about_title_ru',
                'about_text_ru',
                'address_ru'
            )
        }),
        ('Fallback Content', {
            'classes': ('collapse',),
            'fields': (
                'hero_title',
                'hero_subtitle',
                'about_title',
                'about_text',
                'address'
            )
        }),
    )

    def has_add_permission(self, request):
        if HotelInformation.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'description', 'icon')
    list_filter = ('is_active',)
    ordering = ('sort_order', 'name')
    fieldsets = (
        ('Shared Settings', {
            'fields': ('icon', 'sort_order', 'is_active')
        }),
        ('English Content', {
            'fields': ('name_en', 'description_en')
        }),
        ('Uzbek Content', {
            'fields': ('name_uz', 'description_uz')
        }),
        ('Russian Content', {
            'fields': ('name_ru', 'description_ru')
        }),
        ('Fallback Content', {
            'classes': ('collapse',),
            'fields': ('name', 'description')
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'alt_text', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'title_en', 'title_uz', 'title_ru', 'alt_text')
    ordering = ('sort_order', 'id')
    fieldsets = (
        ('Shared Settings', {
            'fields': ('image', 'category', 'sort_order', 'is_active')
        }),
        ('English Content', {
            'fields': ('title_en', 'alt_text_en')
        }),
        ('Uzbek Content', {
            'fields': ('title_uz', 'alt_text_uz')
        }),
        ('Russian Content', {
            'fields': ('title_ru', 'alt_text_ru')
        }),
        ('Fallback Content', {
            'classes': ('collapse',),
            'fields': ('title', 'alt_text')
        }),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'valid_from', 'valid_until', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_until')
    search_fields = ('title', 'title_en', 'title_uz', 'title_ru', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', 'id')
    fieldsets = (
        ('Shared Settings', {
            'fields': ('slug', 'image', 'valid_from', 'valid_until', 'sort_order', 'is_active')
        }),
        ('English Content', {
            'fields': ('title_en', 'short_description_en', 'description_en')
        }),
        ('Uzbek Content', {
            'fields': ('title_uz', 'short_description_uz', 'description_uz')
        }),
        ('Russian Content', {
            'fields': ('title_ru', 'short_description_ru', 'description_ru')
        }),
        ('Fallback Content', {
            'classes': ('collapse',),
            'fields': ('title', 'short_description', 'description')
        }),
    )
