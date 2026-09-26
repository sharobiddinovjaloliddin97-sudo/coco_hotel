from django.contrib import admin
from .models import CallbackRequest, ContactMessage


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'preferred_time',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = (
        'full_name',
        'phone',
        'message',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    actions = ['mark_as_contacted', 'mark_as_closed']

    @admin.action(description="Mark selected callback requests as CONTACTED", permissions=['change'])
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='CONTACTED')
        if request:
            self.message_user(request, f"{updated} callback request(s) marked as CONTACTED.")

    @admin.action(description="Mark selected callback requests as CLOSED", permissions=['change'])
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='CLOSED')
        if request:
            self.message_user(request, f"{updated} callback request(s) marked as CLOSED.")
    fieldsets = (
        ('Guest', {
            'fields': (
                'full_name',
                'phone',
                'preferred_time',
            )
        }),
        ('Request', {
            'fields': (
                'message',
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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'phone',
        'subject',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'created_at',
    )
    search_fields = (
        'full_name',
        'email',
        'phone',
        'subject',
        'message',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    actions = ['mark_as_contacted', 'mark_as_closed']

    @admin.action(description="Mark selected contact messages as CONTACTED", permissions=['change'])
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='CONTACTED')
        if request:
            self.message_user(request, f"{updated} contact message(s) marked as CONTACTED.")

    @admin.action(description="Mark selected contact messages as CLOSED", permissions=['change'])
    def mark_as_closed(self, request, queryset):
        updated = queryset.update(status='CLOSED')
        if request:
            self.message_user(request, f"{updated} contact message(s) marked as CLOSED.")
    fieldsets = (
        ('Guest', {
            'fields': (
                'full_name',
                'email',
                'phone',
            )
        }),
        ('Message', {
            'fields': (
                'subject',
                'message',
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
