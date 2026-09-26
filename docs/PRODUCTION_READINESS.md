# Coco Hotel — implementation handoff

Branch: feature/production-readiness. Based on develop at d4535a5.
Do not deploy until the service credentials and real hotel content are configured.

## Completed

- Responsive editorial homepage, dark/light themes, UZ/RU/EN text coverage.
- Fixed About page runtime crash; enabled undefined-variable lint checks.
- Removed fabricated room ratings and unrelated stock-photo fallbacks.
- Admin-managed homepage/story images and gallery categories (migration 0005).
- Public pages read Django APIs; empty/error states remain honest.
- Gallery keyboard activation, Escape dismissal, focus restoration and focus trap.
- Booking submission/capacity checks, local calendar dates, spam honeypot and phone validation.
- Existing historical requests can be completed by staff after the stay.
- Supabase S3 media storage; local development storage remains available.
- Production secret validation, secure cookies, HTTPS redirect, proxy configuration,
  WhiteNoise admin static files, Gunicorn, Vercel SPA rewrites.
- Frontend build requires its API URL; GitHub CI uses a PostgreSQL service.
- Optional Redis-backed throttling configuration for multiple backend workers.

## Supabase Storage setup

Use a dedicated PUBLIC bucket named coco-media, containing hotel publicity images
only. Do not upload guest documents. Configure bucket limits for accepted image
MIME types and a reasonable maximum upload size. Public reading does not require
anonymous upload/update/delete policies; leave those unavailable to visitors.

Django Admin uploads through S3 credentials stored ONLY in backend environment
variables. These are S3 Access Key ID / Secret Access Key, not the anon key and
not a frontend VITE_ variable. Copy the endpoint and region from the project's
S3 configuration; do not guess the region.

Set:

- MEDIA_STORAGE=supabase
- SUPABASE_S3_ENDPOINT_URL (from Supabase S3 settings)
- SUPABASE_S3_REGION (from the same settings)
- SUPABASE_S3_ACCESS_KEY_ID
- SUPABASE_S3_SECRET_ACCESS_KEY
- SUPABASE_STORAGE_BUCKET=coco-media
- SUPABASE_PUBLIC_MEDIA_URL=https://PROJECT_REF.supabase.co/storage/v1/object/public/coco-media

References:
https://supabase.com/docs/guides/storage/s3/authentication
https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

Switching storage does not move old local media files. Re-upload old photos from
Django Admin or migrate the files preserving their stored paths. Do not delete
old files before confirming that every image loads from the new storage.

## Local setup

Backend, from backend/:

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with the verified Neon DEV connection and DEBUG=True.
python manage.py migrate
python manage.py setup_hotel_groups
python manage.py createsuperuser
python manage.py runserver
```

Install dependencies, prepare environment, apply migrations, create staff roles,
create the administrator, and start Django in that order. Never reset a database.

Frontend, in a second terminal from frontend/:

```powershell
npm ci
Copy-Item .env.example .env
npm run dev
```

This starts Vite using http://127.0.0.1:8000/api/v1 by default.

## Content and admin acceptance

1. Create/edit Hotel Information: contacts, address, map URL, three translations,
   check-in/out times, homepage image and story image.
2. Add real rooms with prices in UZS, capacities, images and amenities.
3. Set featured rooms, active services, gallery categories and promotion dates.
4. Submit a booking from the website; confirm it appears as NEW in Django Admin.
5. Staff review availability externally, then mark CONTACTED/CONFIRMED as appropriate.
6. Verify a contact message and callback request in the admin panel.
7. Confirm each uploaded photo loads from Supabase after restarting the backend.

Bookings remain inquiries reviewed by staff. There is no automatic room inventory
allocation or online payment, and no Telegram/email notifications were requested.

## Deployment later

Backend root: backend. Set DEBUG=False, strong random SECRET_KEY (50+ characters),
DATABASE_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, CSRF_TRUSTED_ORIGINS and media
settings. Enable TRUST_PROXY_SSL_HEADER only behind a trusted sanitizing proxy.
Keep HSTS at zero until HTTPS is verified. Configure REDIS_URL for shared throttling.

```sh
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py setup_hotel_groups
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --access-logfile -
```

These collect assets, apply reviewed migrations, create roles and start the server.
Use an interactive createsuperuser command for the administrator.

Frontend root: frontend; set VITE_API_BASE_URL to the HTTPS backend /api/v1 URL,
VITE_SITE_URL to its real domain. Run npm ci and npm run build; publish dist.
The included vercel.json supports direct navigation and page refreshes.

## Verification boundaries

Automated local tests use isolated SQLite and mocked frontend API responses.
PostgreSQL CI is configured but must run on GitHub. Live Supabase upload, Neon
connectivity and hosted end-to-end flows require the owner's configuration.
No cloud database was changed and no deployment was performed.
Before launch verify backups/restoration, real content, domains and privacy text
appropriate to the hotel's handling of guest contact information.
