"""Home page models with StreamField and SEO support."""
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from .blocks import ContentStreamBlock


class HomePage(Page):
    """Landing page with flexible StreamField content."""
    subtitle = models.CharField(max_length=200, blank=True)
    body = StreamField(ContentStreamBlock(), blank=True, use_json_field=True)

    # SEO fields
    seo_description = models.TextField(
        blank=True, max_length=300,
        help_text="Override default meta description for SEO",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_description"),
    ]

    api_fields = [
        APIField("subtitle"),
        APIField("body"),
    ]

    subpage_types = ["blog.BlogIndexPage", "services.ServicePage", "home.FlexPage"]
    max_count = 1

    class Meta:
        verbose_name = "Home Page"


class FlexPage(Page):
    """Generic flexible page for any content (About, Contacts, etc.)."""
    body = StreamField(ContentStreamBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    api_fields = [APIField("body")]

    parent_page_types = ["home.HomePage"]

    class Meta:
        verbose_name = "Flexible Page"


@register_setting
class SiteSettings(BaseSiteSetting):
    """Global site settings editable from Wagtail admin."""
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True, default="10:00 - 20:00")
    google_maps_embed = models.TextField(
        blank=True, help_text="Google Maps iframe embed code"
    )

    panels = [
        MultiFieldPanel([
            FieldPanel("phone"),
            FieldPanel("email"),
            FieldPanel("address"),
            FieldPanel("working_hours"),
        ], heading="Contact Info"),
        MultiFieldPanel([
            FieldPanel("instagram_url"),
            FieldPanel("facebook_url"),
            FieldPanel("tiktok_url"),
        ], heading="Social Media"),
        FieldPanel("google_maps_embed"),
    ]

    class Meta:
        verbose_name = "Site Settings"
