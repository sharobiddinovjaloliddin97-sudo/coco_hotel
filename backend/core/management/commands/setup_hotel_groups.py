from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


RECEPTIONIST_PERMISSIONS = [
    # Operational: Bookings
    ('bookings', 'bookingrequest', 'view_bookingrequest'),
    ('bookings', 'bookingrequest', 'change_bookingrequest'),
    # Operational: Callback Requests
    ('guest_requests', 'callbackrequest', 'view_callbackrequest'),
    ('guest_requests', 'callbackrequest', 'change_callbackrequest'),
    # Operational: Contact Messages
    ('guest_requests', 'contactmessage', 'view_contactmessage'),
    ('guest_requests', 'contactmessage', 'change_contactmessage'),
    # Read-only reference for rooms and amenities in admin
    ('rooms', 'room', 'view_room'),
    ('rooms', 'amenity', 'view_amenity'),
]

MANAGER_PERMISSIONS = [
    # Operational: Bookings
    ('bookings', 'bookingrequest', 'view_bookingrequest'),
    ('bookings', 'bookingrequest', 'change_bookingrequest'),
    # Operational: Callback Requests
    ('guest_requests', 'callbackrequest', 'view_callbackrequest'),
    ('guest_requests', 'callbackrequest', 'change_callbackrequest'),
    # Operational: Contact Messages
    ('guest_requests', 'contactmessage', 'view_contactmessage'),
    ('guest_requests', 'contactmessage', 'change_contactmessage'),
    # Content: Rooms
    ('rooms', 'room', 'view_room'),
    ('rooms', 'room', 'add_room'),
    ('rooms', 'room', 'change_room'),
    # Content: Room Images
    ('rooms', 'roomimage', 'view_roomimage'),
    ('rooms', 'roomimage', 'add_roomimage'),
    ('rooms', 'roomimage', 'change_roomimage'),
    ('rooms', 'roomimage', 'delete_roomimage'),
    # Content: Amenities
    ('rooms', 'amenity', 'view_amenity'),
    ('rooms', 'amenity', 'add_amenity'),
    ('rooms', 'amenity', 'change_amenity'),
    ('rooms', 'amenity', 'delete_amenity'),
    # Content: Hotel Information
    ('hotel', 'hotelinformation', 'view_hotelinformation'),
    ('hotel', 'hotelinformation', 'add_hotelinformation'),
    ('hotel', 'hotelinformation', 'change_hotelinformation'),
    # Content: Services
    ('hotel', 'service', 'view_service'),
    ('hotel', 'service', 'add_service'),
    ('hotel', 'service', 'change_service'),
    ('hotel', 'service', 'delete_service'),
    # Content: Gallery
    ('hotel', 'galleryimage', 'view_galleryimage'),
    ('hotel', 'galleryimage', 'add_galleryimage'),
    ('hotel', 'galleryimage', 'change_galleryimage'),
    ('hotel', 'galleryimage', 'delete_galleryimage'),
    # Content: Promotions
    ('hotel', 'promotion', 'view_promotion'),
    ('hotel', 'promotion', 'add_promotion'),
    ('hotel', 'promotion', 'change_promotion'),
    ('hotel', 'promotion', 'delete_promotion'),
]


class Command(BaseCommand):
    help = "Idempotently configure Receptionist and Manager staff groups and permissions."

    def handle(self, *args, **options):
        self.stdout.write("Configuring hotel staff roles and permissions...")

        roles = {
            'Receptionist': RECEPTIONIST_PERMISSIONS,
            'Manager': MANAGER_PERMISSIONS,
        }

        for role_name, perm_specs in roles.items():
            group, created = Group.objects.get_or_create(name=role_name)
            action_label = "Created" if created else "Found existing"

            resolved_perms = []
            missing_specs = []

            for app_label, model, codename in perm_specs:
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    resolved_perms.append(permission)
                except (ContentType.DoesNotExist, Permission.DoesNotExist):
                    missing_specs.append(f"{app_label}.{codename}")

            if missing_specs:
                self.stderr.write(
                    self.style.WARNING(
                        f"Warning: Missing permissions for {role_name}: {', '.join(missing_specs)}"
                    )
                )

            # Set exact intended permissions; automatically purges any unintended permissions
            group.permissions.set(resolved_perms)

            self.stdout.write(
                self.style.SUCCESS(
                    f"{action_label} group '{role_name}' with {len(resolved_perms)} permissions."
                )
            )

        self.stdout.write(self.style.SUCCESS("Hotel staff groups setup completed successfully."))
