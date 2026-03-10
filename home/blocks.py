"""Custom StreamField blocks for flexible page content."""
from wagtail.blocks import (
    CharBlock, RichTextBlock, StructBlock, ListBlock,
    URLBlock, ChoiceBlock, TextBlock, PageChooserBlock,
    StreamBlock,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


class HeroBlock(StructBlock):
    """Full-width hero section with background image and CTA."""
    heading = CharBlock(max_length=120, help_text="Main heading text")
    subheading = TextBlock(required=False, help_text="Supporting text below heading")
    background_image = ImageChooserBlock()
    cta_text = CharBlock(max_length=40, required=False, label="Button text")
    cta_link = PageChooserBlock(required=False, label="Button link")
    overlay_opacity = ChoiceBlock(
        choices=[
            ("0.3", "Light"), ("0.5", "Medium"), ("0.7", "Dark"),
        ],
        default="0.5",
        help_text="Darkness of overlay on background image",
    )

    class Meta:
        icon = "image"
        template = "blocks/hero_block.html"
        label = "Hero Section"


class ServiceCardBlock(StructBlock):
    """Single service card with icon, title, description."""
    title = CharBlock(max_length=80)
    description = TextBlock()
    icon = ChoiceBlock(
        choices=[
            ("tattoo", "Tattoo"), ("piercing", "Piercing"),
            ("removal", "Laser Removal"), ("design", "Custom Design"),
            ("consultation", "Consultation"), ("touch-up", "Touch-up"),
        ],
    )
    image = ImageChooserBlock(required=False)
    page_link = PageChooserBlock(required=False, help_text="Link to service detail page")

    class Meta:
        icon = "list-ul"
        template = "blocks/service_card.html"


class ServicesGridBlock(StructBlock):
    """Grid of service cards."""
    heading = CharBlock(max_length=100, default="Our Services")
    services = ListBlock(ServiceCardBlock())
    columns = ChoiceBlock(
        choices=[("2", "2 columns"), ("3", "3 columns"), ("4", "4 columns")],
        default="3",
    )

    class Meta:
        icon = "grip"
        template = "blocks/services_grid.html"
        label = "Services Grid"


class TestimonialBlock(StructBlock):
    """Client testimonial with photo and rating."""
    client_name = CharBlock(max_length=80)
    client_photo = ImageChooserBlock(required=False)
    text = TextBlock()
    rating = ChoiceBlock(
        choices=[(str(i), f"{i} stars") for i in range(1, 6)],
        default="5",
    )

    class Meta:
        icon = "openquote"
        template = "blocks/testimonial.html"


class GalleryBlock(StructBlock):
    """Photo gallery with lightbox support."""
    heading = CharBlock(max_length=100, required=False)
    images = ListBlock(
        StructBlock([
            ("image", ImageChooserBlock()),
            ("caption", CharBlock(max_length=200, required=False)),
            ("style", ChoiceBlock(
                choices=[
                    ("blackwork", "Blackwork"), ("realism", "Realism"),
                    ("traditional", "Traditional"), ("watercolor", "Watercolor"),
                    ("geometric", "Geometric"), ("japanese", "Japanese"),
                    ("other", "Other"),
                ],
                required=False,
            )),
        ])
    )

    class Meta:
        icon = "image"
        template = "blocks/gallery.html"
        label = "Portfolio Gallery"


class FAQBlock(StructBlock):
    """Collapsible FAQ item."""
    question = CharBlock(max_length=200)
    answer = RichTextBlock(features=["bold", "italic", "link", "ul"])

    class Meta:
        icon = "help"
        template = "blocks/faq.html"


class CTABlock(StructBlock):
    """Call-to-action banner."""
    heading = CharBlock(max_length=120)
    text = TextBlock(required=False)
    button_text = CharBlock(max_length=40, default="Book Now")
    button_link = URLBlock(required=False)
    style = ChoiceBlock(
        choices=[("primary", "Primary"), ("dark", "Dark"), ("gradient", "Gradient")],
        default="primary",
    )

    class Meta:
        icon = "plus-inverse"
        template = "blocks/cta.html"
        label = "Call to Action"


class ContentStreamBlock(StreamBlock):
    """Main content stream used across multiple page types."""
    hero = HeroBlock()
    rich_text = RichTextBlock(
        features=["h2", "h3", "bold", "italic", "link", "ul", "ol", "image", "embed"],
        icon="pilcrow",
    )
    services_grid = ServicesGridBlock()
    gallery = GalleryBlock()
    testimonial = ListBlock(TestimonialBlock(), icon="openquote", label="Testimonials")
    faq = ListBlock(FAQBlock(), icon="help", label="FAQ Section")
    cta = CTABlock()
    embed = EmbedBlock(icon="media", label="Video / Embed")
