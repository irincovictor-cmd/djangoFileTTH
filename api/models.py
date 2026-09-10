from django.db import models


class Topic(models.Model):
    """
    One educational topic shown on the Topics page.
    Data lives in the database — not hard-coded in the HTML.
    """

    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, help_text="Short label, e.g. Django, Git")
    summary = models.TextField(help_text="Short description on the topics list")
    body = models.TextField(help_text="Longer explanation on the detail page")

    resource_url = models.URLField(
        blank=True,
        help_text="Link to docs or a video for deeper study (leave blank if none)",
    )
    resource_label = models.CharField(
        max_length=100,
        blank=True,
        default="Learn more",
        help_text="Button text, e.g. Official Django docs",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Contact(models.Model):
    """
    One contact form submission (name, email, phone).
    Saved when ContactForm is valid and form.save() runs.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(
        max_length=30,
        verbose_name="Contact number",
        help_text="Phone or mobile number",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
