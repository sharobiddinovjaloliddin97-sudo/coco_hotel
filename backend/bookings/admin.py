from django.contrib import admin
from .models import BookingRequest


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'room',
        'check_in',
        'check_out',
        'adults',
        'children',
        'phone',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'room',
        'check_in',
        'check_out',
        'created_at',
    )
    search_fields = (
        'full_name',
        'phone',
        'email',
        'room_name_snapshot',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'room_name_snapshot',
        'price_per_night_snapshot',
        'created_at',
        'updated_at',
    )
    actions = [
        'mark_as_contacted',
        'mark_as_confirmed',
        'mark_as_cancelled',
        'mark_as_completed',
    ]

    @admin.action(description="Mark selected booking requests as CONTACTED", permissions=['change'])
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='CONTACTED')
        if request:
            self.message_user(request, f"{updated} booking request(s) marked as CONTACTED.")

    @admin.action(description="Mark selected booking requests as CONFIRMED", permissions=['change'])
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='CONFIRMED')
        if request:
            self.message_user(request, f"{updated} booking request(s) marked as CONFIRMED.")

    @admin.action(description="Mark selected booking requests as CANCELLED", permissions=['change'])
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        if request:
            self.message_user(request, f"{updated} booking request(s) marked as CANCELLED.")

    @admin.action(description="Mark selected booking requests as COMPLETED", permissions=['change'])
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        if request:
            self.message_user(request, f"{updated} booking request(s) marked as COMPLETED.")
    fieldsets = (
        ('Guest', {
            'fields': (
                'full_name',
                'phone',
                'email',
            )
        }),
        ('Stay', {
            'fields': (
                'room',
                'room_name_snapshot',
                'price_per_night_snapshot',
                'check_in',
                'check_out',
                'adults',
                'children',
            )
        }),
        ('Request', {
            'fields': (
                'special_request',
            )
        }),
        ('Management', {
            'fields': (
                'status',
                'admin_note',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
