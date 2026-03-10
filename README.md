# Wagtail Tattoo Studio CMS

Content management system for a tattoo studio chain, built with **Wagtail CMS 7.2** and **Django 5**.

## Features

- **StreamField content** — flexible page builder with custom blocks (Hero, Gallery, Services Grid, FAQ, CTA, Testimonials)
- **Custom Page models** — HomePage, FlexPage, BlogPage, ServicePage with full admin panel configuration
- **Blog system** — categories (snippets), tags, pagination, filtering, reading time
- **Service pages** — pricing tiers, artist profiles, booking integration
- **Wagtail API v2** — headless CMS endpoints for pages, images, documents
- **Site Settings** — global contacts, social media, working hours via Wagtail admin
- **SEO-ready** — meta descriptions, structured content, semantic HTML
- **Docker-ready** — Dockerfile + Redis caching

## Tech Stack

| Layer | Technology |
|-------|-----------|
| CMS | Wagtail 7.2 |
| Backend | Django 5, Python 3.12 |
| Cache | Redis |
| Frontend | Bootstrap 5, Vanilla JS |
| Deploy | Docker, Gunicorn |

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin panel: `http://localhost:8000/admin/`

## Project Structure

```
├── home/           # HomePage, FlexPage, SiteSettings, custom blocks
│   ├── blocks.py   # StreamField blocks (Hero, Gallery, FAQ, CTA...)
│   ├── models.py   # Page models + site settings
│   └── templatetags/site_tags.py
├── blog/           # Blog with categories, tags, pagination
│   └── models.py   # BlogIndexPage, BlogPage, BlogCategory snippet
├── services/       # Service pages + artist profiles
│   └── models.py   # ServicePage, PricingTier, TattooArtist snippet
└── tattoo_cms/     # Project config
    ├── settings.py
    ├── urls.py
    └── api.py      # Wagtail API v2 router
```
