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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
