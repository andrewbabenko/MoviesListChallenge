from functools import reduce
from movie_list.settings import STUDIO_GHIBLI_FILMS_ENDPOINT


class FilmsInformationComposer:
    """ Compose films information """

    def __init__(self, films_data: list, characters_data: list):
        self.films_data = films_data
        self.characters_data = characters_data
        self.films_storage = {}

    @staticmethod
    def _extract_film_id(film_url: str) -> str:
        """ Extract film id from URL.
        Example of URL:

        :param film_url: link to particular film data
        :return: film id
        """
        return film_url.replace(f'{STUDIO_GHIBLI_FILMS_ENDPOINT}/', '')

    @staticmethod
    def __films_data_reducer(films_storage: dict, film_data: dict) -> dict:
        """ Fill films_storage with data from film_data.

        :param films_storage: storage with films information
        :param film_data: information about particular film
        :return: films_storage updated with given film data
        """
        films_storage[film_data['id']] = {
            'people': [],
            'title': film_data['title']
        }

        return films_storage

    def __characters_data_mapper(self, character_data: dict):
        """ Map character data to each particular film, where character appearing in

        :param character_data: character name and films, where character appearing in
        """
        for film_url in character_data['films']:
            film_id = FilmsInformationComposer._extract_film_id(film_url)
            self.films_storage[film_id]['people'].append(character_data['name'])

    def compose(self) -> dict:
        """ Create a storage with films and it's characters """
        reduce(FilmsInformationComposer.__films_data_reducer, self.films_data, self.films_storage)
        _ = [*map(self.__characters_data_mapper, self.characters_data)]

        return self.films_storage
