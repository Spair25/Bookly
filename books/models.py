from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)

    author = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    first_publish_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    open_library_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Edition(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('uk', 'Українська'),
        ('ru', 'Русский'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='editions'
    )

    title = models.CharField(max_length=255)

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    isbn = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True
    )

    publisher = models.CharField(
        max_length=255,
        blank=True
    )

    publish_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    cover_url = models.URLField(
        max_length=500,
        blank=True
    )

    open_library_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.language})"