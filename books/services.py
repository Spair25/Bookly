import requests
from django.core.cache import cache


OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

LANGUAGE_CODES = {
    "en": "eng",
    "uk": "ukr",
    "ru": "rus",
}


def search_books(query, limit=12, language="all"):
    if not query.strip():
        return []

    params = {
        "q": query,
        "limit": limit,
        "fields": "key,title,author_name,first_publish_year,cover_i,language",
    }

    if language in LANGUAGE_CODES:
        params["lang"] = LANGUAGE_CODES[language]
        params["q"] = (
            f"{query} language:{LANGUAGE_CODES[language]}"
        )

    try:
        response = requests.get(
            OPEN_LIBRARY_URL,
            params=params,
            timeout=10,
            headers={
                "User-Agent": "Bookly/0.1 (local development)"
            }
        )

        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Open Library API error: {error}")
        return []

    books = []

    for item in data.get("docs", []):
        cover_id = item.get("cover_i")

        cover_url = (
            f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            if cover_id else None
        )

        books.append({
            "open_library_id": item.get("key"),
            "title": item.get("title", "Unknown title"),
            "author": ", ".join(
                item.get("author_name", ["Unknown author"])
            ),
            "year": item.get("first_publish_year"),
            "cover_url": cover_url,
            "languages": item.get("language", []),
        })

    return books
def get_book_details(open_library_id):
    if not open_library_id.startswith("/works/"):
        return None

    url = f"https://openlibrary.org{open_library_id}.json"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Bookly/0.1 (local development)"
            }
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Open Library details error: {error}")
        return None

    description = data.get("description", "")

    if isinstance(description, dict):
        description = description.get("value", "")

    covers = data.get("covers", [])

    cover_url = None

    if covers:
        cover_url = (
            f"https://covers.openlibrary.org/b/id/"
            f"{covers[0]}-L.jpg"
        )

    return {
        "open_library_id": open_library_id,
        "title": data.get("title", "Unknown title"),
        "description": description,
        "cover_url": cover_url,
        "first_publish_date": data.get("first_publish_date"),
    }
def get_book_editions(open_library_id, limit=1000):
    if not open_library_id.startswith("/works/"):
        return []
    cache_key = f"book_editions:{open_library_id}:{limit}"

    cached_editions = cache.get(cache_key)

    if cached_editions is not None:
        return cached_editions


    url = f"https://openlibrary.org{open_library_id}/editions.json"

    language_codes = {
        "eng": "en",
        "ukr": "uk",
        "rus": "ru",
    }

    editions = []
    offset = 0
    page_size = 100
    total_available = None

    while offset < limit:
        try:
            response = requests.get(
                url,
                params={
                    "limit": min(page_size, limit - offset),
                    "offset": offset,
                },
                timeout=20,
                headers={
                    "User-Agent": "Bookly/0.1 (local development)"
                }
            )

            response.raise_for_status()
            data = response.json()
            total_available = data.get("size")

        except (requests.RequestException, ValueError) as error:
            print(f"Open Library editions error: {error}")
            break

        entries = data.get("entries", [])

        print(
            f"Loaded {len(entries)} editions "
            f"at offset {offset}"
        )

        if not entries:
            break

        for item in entries:
            for language in item.get("languages", []):
                code = language.get("key", "").split("/")[-1]

                if code not in language_codes:
                    continue

                covers = item.get("covers") or []
                cover_id = next(
                    (
                        cover for cover in covers
                        if isinstance(cover, int) and cover > 0
                    ),
                    None
                )

                cover_url = (
                    f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    if cover_id else None
                )

                isbn_13 = item.get("isbn_13") or []
                isbn_10 = item.get("isbn_10") or []

                isbn = (
                    isbn_13[0] if isbn_13
                    else isbn_10[0] if isbn_10
                    else None
                )

                editions.append({
                    "open_library_id": item.get("key"),
                    "title": item.get("title", "Unknown title"),
                    "language": language_codes[code],
                    "publish_date": item.get("publish_date", ""),
                    "cover_url": cover_url,
                    "isbn": isbn,
                })

        offset += len(entries)

        if offset >= data.get("size", 0):
            break
    
    if total_available is not None and offset >= total_available:
        cache.set(cache_key, editions, timeout=60 * 60 * 24)

    return editions

    
