from django.db import migrations

INITIAL_SERVICES = [
    {
        "name": "Wi-Fi",
        "icon": "wifi",
        "description": "Complimentary high-speed wireless internet access across all rooms and common areas.",
        "sort_order": 1,
    },
    {
        "name": "Breakfast",
        "icon": "coffee",
        "description": "Fresh and nourishing daily breakfast buffet.",
        "sort_order": 2,
    },
    {
        "name": "Parking",
        "icon": "car",
        "description": "Secure on-site guest parking.",
        "sort_order": 3,
    },
    {
        "name": "24/7 Reception",
        "icon": "clock",
        "description": "Around-the-clock front desk and guest concierge service.",
        "sort_order": 4,
    },
    {
        "name": "Daily Cleaning",
        "icon": "sparkles",
        "description": "Daily housekeeping and fresh towel replenishment.",
        "sort_order": 5,
    },
    {
        "name": "Air Conditioning",
        "icon": "snowflake",
        "description": "Individually controlled climate cooling and heating.",
        "sort_order": 6,
    },
]


def seed_services(apps, schema_editor):
    Service = apps.get_model('hotel', 'Service')
    for svc_data in INITIAL_SERVICES:
        Service.objects.get_or_create(
            name=svc_data["name"],
            defaults={
                "icon": svc_data["icon"],
                "description": svc_data["description"],
                "sort_order": svc_data["sort_order"],
                "is_active": True,
            }
        )


def unseed_services(apps, schema_editor):
    Service = apps.get_model('hotel', 'Service')
    service_names = [s["name"] for s in INITIAL_SERVICES]
    Service.objects.filter(name__in=service_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services, reverse_code=unseed_services),
    ]
