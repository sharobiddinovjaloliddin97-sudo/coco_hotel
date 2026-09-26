from django.contrib import admin
from rooms.models import Amenity, Room, RoomImage


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'sort_order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'icon')
    ordering = ('sort_order', 'name')
    list_editable = ('sort_order', 'is_active')
    fieldsets = (
        ('Shared Settings', {
            'fields': ('name', 'icon', 'sort_order', 'is_active')
        }),
        ('Translations', {
            'fields': ('name_en', 'name_uz', 'name_ru')
        }),
    )


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'sort_order')
    ordering = ('sort_order', 'id')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price_per_night',
        'max_adults',
        'max_children',
        'bed_type',
        'room_size',
        'is_featured',
        'is_active',
        'sort_order',
    )
    list_filter = ('is_active', 'is_featured', 'bed_type')
    search_fields = ('name', 'name_en', 'name_uz', 'name_ru', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('amenities',)
    ordering = ('sort_order', 'name')
    list_editable = ('price_per_night', 'is_featured', 'is_active', 'sort_order')
    inlines = [RoomImageInline]
    fieldsets = (
        ('Shared Settings', {
            'fields': (
                'slug',
                'price_per_night',
                'max_adults',
                'max_children',
                'room_size',
                'amenities',
                'is_featured',
                'is_active',
                'sort_order',
            )
        }),
        ('English Content', {
            'fields': ('name_en', 'short_description_en', 'description_en', 'bed_type_en')
        }),
        ('Uzbek Content', {
            'fields': ('name_uz', 'short_description_uz', 'description_uz', 'bed_type_uz')
        }),
        ('Russian Content', {
            'fields': ('name_ru', 'short_description_ru', 'description_ru', 'bed_type_ru')
        }),
        ('Fallback Content', {
            'classes': ('collapse',),
            'fields': ('name', 'short_description', 'description', 'bed_type')
        }),
    )


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image', 'alt_text', 'is_primary', 'sort_order')
    list_filter = ('is_primary', 'room')
    search_fields = ('room__name', 'alt_text')
    ordering = ('room', 'sort_order')
