"""Custom template tags for site-wide use."""
from django import template
from wagtail.models import Site
from home.models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_settings(context):
    """Get global site settings in templates: {% get_site_settings as settings %}"""
    request = context.get("request")
    if request:
        site = Site.find_for_request(request)
        return SiteSettings.for_site(site)
    return None


@register.filter
def reading_time_display(minutes):
    """Format reading time: {{ post.reading_time|reading_time_display }}"""
    if minutes <= 1:
        return "1 min read"
    return f"{minutes} min read"
