import requests

from django.core.cache import cache

from movie_list.settings import (
    STUDIO_GHIBLI_FILMS_ENDPOINT,
    STUDIO_GHIBLI_PEOPLE_ENDPOINT,
    STUDIO_GHIBLI_URL,
    STORE_CACHE_FOR
)
from studio_ghibli.data_composers import FilmsInformationComposer


def get_films_data() -> dict:
    """ Get a list of films with required description. If films data exists at cache -
    return cached data. Otherwise collect data from an API, save it to the cache with
    storing timeout = 1 min and return collected movies data
    """
    films_data = cache.get(STUDIO_GHIBLI_URL)

    if not films_data:
        response_films = requests.get(f"{STUDIO_GHIBLI_FILMS_ENDPOINT}?limit=250&fields=id,title")
        response_characters = requests.get(f"{STUDIO_GHIBLI_PEOPLE_ENDPOINT}?limit=250&fields=name,films")

        response_films.raise_for_status()
        response_characters.raise_for_status()

        films_composer = FilmsInformationComposer(response_films.json(), response_characters.json())
        films_data = films_composer.compose()

        cache.set(STUDIO_GHIBLI_URL, films_data, STORE_CACHE_FOR)

    return films_data
