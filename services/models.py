"""Service pages with pricing, booking integration, and artist profiles."""
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet

from home.blocks import ContentStreamBlock


@register_snippet
class TattooArtist(models.Model):
    """Artist profile as reusable snippet."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    bio = RichTextField(blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    instagram = models.URLField(blank=True)
    specializations = models.CharField(
        max_length=300, blank=True,
        help_text="Comma-separated: Realism, Blackwork, Japanese...",
    )
    years_experience = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"), FieldPanel("slug"), FieldPanel("photo"),
        ], heading="Basic Info"),
        FieldPanel("bio"),
        MultiFieldPanel([
            FieldPanel("specializations"), FieldPanel("years_experience"),
            FieldPanel("instagram"), FieldPanel("is_active"),
        ], heading="Details"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ServicePage(Page):
    """Individual service page (Tattoo, Piercing, Removal, etc.)."""
    description = RichTextField(blank=True)
    body = StreamField(ContentStreamBlock(), blank=True, use_json_field=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class")
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    booking_url = models.URLField(blank=True, help_text="External booking system URL")
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Starting price in UAH",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("description"),
            FieldPanel("header_image"),
            FieldPanel("icon"),
        ], heading="Service Overview"),
        FieldPanel("body"),
        MultiFieldPanel([
            FieldPanel("min_price"),
            FieldPanel("booking_url"),
        ], heading="Pricing & Booking"),
        InlinePanel("pricing_tiers", label="Pricing Tiers"),
    ]

    api_fields = [
        APIField("description"), APIField("body"),
        APIField("min_price"), APIField("booking_url"),
    ]

    parent_page_types = ["home.HomePage"]

    class Meta:
        verbose_name = "Service Page"


class PricingTier(Orderable):
    """Pricing tier for a service (e.g., Small tattoo, Medium, Full sleeve)."""
    page = ParentalKey(ServicePage, on_delete=models.CASCADE, related_name="pricing_tiers")
    name = models.CharField(max_length=100, help_text="e.g., 'Small (up to 10cm)'")
    price = models.CharField(max_length=50, help_text="e.g., 'від 1500 грн' or '2000-5000 грн'")
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., '1-2 hours'")
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("name"), FieldPanel("price"),
        FieldPanel("duration"), FieldPanel("description"),
    ]
