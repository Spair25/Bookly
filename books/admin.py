from django.contrib import admin
from .models import Book, Edition


class EditionInline(admin.TabularInline):
    model = Edition
    extra = 0
    fields = (
        'title',
        'language',
        'isbn',
        'publisher',
        'publish_year',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'first_publish_year',
        'created_at',
    )

    search_fields = (
        'title',
        'author',
        'open_library_id',
    )

    list_filter = (
        'first_publish_year',
    )

    readonly_fields = ('created_at',)

    inlines = [EditionInline]


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'book',
        'language',
        'publisher',
        'publish_year',
    )

    search_fields = (
        'title',
        'book__title',
        'isbn',
    )

    list_filter = (
        'language',
        'publish_year',
    )
