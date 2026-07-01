# Kaku Portfolio

A Django-backed portfolio CMS for **Kaku Amsalu**. Two fully content-managed front-end experiences share one database:

- **One Page** (`/`) — a classic vertical-scroll portfolio.
- **Cinematic** (`/cinematic/`) — a horizontal-scroll, panel-by-panel "index" with kinetic typography, a persistent HUD, and per-project frame graphics.

Every visible section — hero, about, services, résumé, skills, projects, contact — is editable from the Django admin. No code change is needed to update content.

---

## Tech stack

- **Python 3.12**, **Django 6.0**
- **PostgreSQL** (via `psycopg` + `DATABASE_URL`); SQLite for quick local runs
- **uv** for dependency management
- **WhiteNoise** for static files in production
- Key Django packages:
  - `django-solo` — singleton models (site settings, hero, about, contact, SEO)
  - `django-ordered-model` — drag-to-sort list items in the admin
  - `django-tinymce` — rich-text fields
  - `django-imagekit` + `Pillow` — image uploads / processing
  - `django-admin-interface` — themed admin
  - `django-cors-headers`, `djangorestframework` — optional API surface
  - `django-environ` — environment-based config

---

## Project structure

```
kaku_portfolio/
├── manage.py
├── pyproject.toml
├── .env                        # local environment (not committed)
├── kaku_portfolio/             # project package
│   ├── settings/               # split settings
│   │   ├── base.py             # shared config
│   │   ├── dev.py              # DEBUG, sqlite, console email
│   │   └── prod.py             # env-driven, security headers, WhiteNoise
│   ├── admin.py                # custom AdminSite with grouped sidebar
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── apps/
│   ├── core/                   # site settings, hero, about, contact, nav, SEO, inbox
│   ├── services/               # service cards
│   ├── resume/                 # education + experience
│   ├── skills/                 # skill groups + ticker
│   ├── projects/               # projects, tags, meta, gallery
│   └── api/                    # optional DRF endpoints
├── templates/
│   ├── base.html
│   ├── one_page.html
│   ├── cinematic.html
│   ├── partials/               # section partials for both pages
│   └── projects/frames/        # per-variant cinematic project graphics
├── static/                     # css/, js/, fonts/
└── media/                      # user uploads
```

---

## Getting started

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
# 1. Install dependencies
uv sync

# 2. Create a .env in the project root (see "Configuration" below)

# 3. Apply migrations
uv run python manage.py migrate

# 4. Create the admin account (single operator — superuser)
uv run python manage.py createsuperuser

# 5. Seed the initial content
uv run python manage.py seed_portfolio

# 6. Run the dev server
uv run python manage.py runserver
```

Then open:

- One Page — http://127.0.0.1:8000/
- Cinematic — http://127.0.0.1:8000/cinematic/
- Admin — http://127.0.0.1:8000/admin/

`manage.py` defaults to the **dev** settings; `wsgi.py`/`asgi.py` default to **prod**. Override anytime with `DJANGO_SETTINGS_MODULE`.

---

## Configuration

Settings are split into `base` / `dev` / `prod` and read from the environment via `django-environ`. Create a `.env` file in the project root:

```dotenv
# Database (Postgres in prod; a sqlite URL works locally)
DATABASE_URL=postgres://user:password@localhost:5432/kaku_portfolio

# Required in production
SECRET_KEY=change-me
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com

# Email (contact-form notifications)
DEFAULT_FROM_EMAIL=no-reply@example.com
CONTACT_EMAIL=you@example.com
```

| Variable | Used by | Notes |
|---|---|---|
| `DATABASE_URL` | all | Postgres URL in prod; SQLite locally |
| `SECRET_KEY` | prod | **Required** in prod (dev has an insecure default) |
| `ALLOWED_HOSTS` | prod | Comma-separated |
| `CSRF_TRUSTED_ORIGINS` | prod | Comma-separated origins |
| `DEFAULT_FROM_EMAIL` | all | Sender for contact notifications |
| `CONTACT_EMAIL` | all | Recipient of contact-form submissions |

Dev uses the console email backend (submissions print to the terminal). Prod expects real SMTP settings.

---

## Managing content

Everything is edited at `/admin/`, where models are grouped in the sidebar as **Identity**, **Content**, **Site**, **Inbox**, and **Administration**.

- **Singletons** — Site Settings, Hero, About, Contact Info, SEO Metadata (one editable record each).
- **Ordered lists** — Services, Education, Experience, Skill Groups, Projects, Nav Links, etc. support drag-to-sort.
- **Rich text** — About paragraphs and project descriptions use a TinyMCE editor.
- **Skills ticker** — the cinematic marquee shows skills flagged `show_in_ticker`, split across two rows (`ticker_row`).
- **Contact inbox** — form submissions are stored and viewable under Inbox; the owner is also emailed.

### Seeding

`python manage.py seed_portfolio` is **idempotent** and populates every section (site settings, hero, about, services, résumé, projects, contact, nav) from the original design content. It intentionally **does not touch skills** — manage those directly in the admin. Re-running it is safe and never creates duplicates.

---

## Front-end notes

- The one-page site scrolls vertically and grows to fit any amount of content.
- The cinematic page is a fixed-viewport horizontal experience. To keep panels from overflowing, the résumé caps at 4 education / 4 experience entries and links to the full list on the one-page.
- The contact form is available on both pages (honeypot-protected) and posts to the same endpoint, returning to whichever page it came from.
- Copyright year renders dynamically from the server clock; project and résumé years are fixed (they are facts).

---

## Deployment

- Set `DJANGO_SETTINGS_MODULE=kaku_portfolio.settings.prod` (default for WSGI/ASGI).
- Provide the required prod env vars (above).
- Collect static files: `python manage.py collectstatic` (served by WhiteNoise with hashed, compressed filenames).
- Prod enables SSL redirect, HSTS, and secure cookies.

---

## Notes

- **Single operator.** This is a one-person site: the owner is the only admin account (a superuser). There is intentionally no role-based access control.
- **Admin hardening** (obscured URL, brute-force lockout, 2FA) is a separate, optional concern from user permissions.
