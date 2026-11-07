from django.shortcuts import render
from .services import search_books
from django.http import Http404
from .services import get_book_details
from .services import get_book_editions


def home_view(request):
    return render(request, 'books/home.html')

def book_search_view(request):
    query = request.GET.get('q', '').strip()
    language = request.GET.get('language', 'all')

    if language not in ('all', 'en', 'uk', 'ru'):
        language = 'all'

    books = []

    if query:
        books = search_books(
            query,
            limit=20,
            language=language
        )

    context = {
        'query': query,
        'books': books,
        'selected_language': language,
    }

    return render(request, 'books/search.html', context)

def book_detail_view(request, work_id):
    book = get_book_details(f"/works/{work_id}")

    if book is None:
        raise Http404("Book not found")

    selected_language = request.GET.get("language", "en")

    if selected_language not in ("en", "uk", "ru"):
        selected_language = "en"

    all_editions = get_book_editions(
        f"/works/{work_id}",
        limit=1000
    )

    editions = [
        edition for edition in all_editions
        if edition["language"] == selected_language
    ]

    available_languages = {
        language: any(
            edition["language"] == language
            for edition in all_editions
        )
        for language in ("en", "uk", "ru")
    }

    context = {
        "book": book,
        "editions": editions,
        "selected_language": selected_language,
        "available_languages": available_languages,
    }

    return render(request, "books/detail.html", context)