"""Blog models with tagging, categories, and pagination."""
from django.db import models
from django.core.paginator import Paginator
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from home.blocks import ContentStreamBlock


@register_snippet
class BlogCategory(models.Model):
    """Blog category as Wagtail snippet for reuse across pages."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    panels = [FieldPanel("name"), FieldPanel("slug"), FieldPanel("description")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage", related_name="tagged_items", on_delete=models.CASCADE)


class BlogIndexPage(Page):
    """Blog listing page with filtering and pagination."""
    intro = RichTextField(blank=True, help_text="Introduction text above post list")
    posts_per_page = models.PositiveIntegerField(default=12)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("posts_per_page"),
    ]

    subpage_types = ["blog.BlogPage"]
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = BlogPage.objects.live().descendant_of(self).order_by("-first_published_at")

        # Filter by category
        category_slug = request.GET.get("category")
        if category_slug:
            posts = posts.filter(categories__slug=category_slug)

        # Filter by tag
        tag = request.GET.get("tag")
        if tag:
            posts = posts.filter(tags__name=tag)

        paginator = Paginator(posts, self.posts_per_page)
        page_num = request.GET.get("page", 1)
        context["posts"] = paginator.get_page(page_num)
        context["categories"] = BlogCategory.objects.all()
        return context

    class Meta:
        verbose_name = "Blog Index"


class BlogPage(Page):
    """Individual blog post with rich content and metadata."""
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short summary for previews")
    header_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    body = StreamField(ContentStreamBlock(), use_json_field=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    reading_time = models.PositiveIntegerField(
        default=5, help_text="Estimated reading time in minutes"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("excerpt"),
            FieldPanel("header_image"),
            FieldPanel("reading_time"),
        ], heading="Post Meta"),
        FieldPanel("body"),
        MultiFieldPanel([
            FieldPanel("categories", widget=models.CheckboxSelectMultiple if False else None),
            FieldPanel("tags"),
        ], heading="Categorization"),
        InlinePanel("gallery_images", label="Gallery Images"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("excerpt"),
        index.SearchField("body"),
    ]

    api_fields = [
        APIField("excerpt"),
        APIField("header_image"),
        APIField("body"),
        APIField("reading_time"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]

    class Meta:
        verbose_name = "Blog Post"


class BlogPageGalleryImage(Orderable):
    """Gallery images attached to a blog post via InlinePanel."""
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey("wagtailimages.Image", on_delete=models.CASCADE, related_name="+")
    caption = models.CharField(max_length=250, blank=True)

    panels = [FieldPanel("image"), FieldPanel("caption")]
