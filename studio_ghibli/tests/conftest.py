import json

from django.test import TestCase
from requests import Response

from movie_list.settings import (
    STUDIO_GHIBLI_FILMS_ENDPOINT,
    STUDIO_GHIBLI_PEOPLE_ENDPOINT,
)


class FakeRequest:
    GET = {}
    POST = {}


class MoviesTestCase(TestCase):

    def setUp(self):
        super().setUp()

    def build_fake_response(self, url, data, status_code=200) -> Response:
        """ Create fake response object

        :param url: request URL
        :param data: data to be added to response
        :param status_code: desired status code for a response
        :return: fake response
        """
        fake_response = Response()
        fake_response.status_code = status_code
        fake_response.url = url
        fake_response.json = lambda: data

        return fake_response

    def fake_api(self, url) -> Response:
        """ Create fake API response

        :param url: URL of requested resource
        :return: fake API response
        """
        if STUDIO_GHIBLI_FILMS_ENDPOINT in url:
            fake_response_data = open(
                "studio_ghibli/tests/resources/responses/films.json",
                "r"
            )

        elif STUDIO_GHIBLI_PEOPLE_ENDPOINT in url:
            fake_response_data = open(
                "studio_ghibli/tests/resources/responses/characters.json",
                "r"
            )
        else:
            raise ValueError(
                f"Request URL should contains one of the following prefixes: "
                f"{STUDIO_GHIBLI_FILMS_ENDPOINT} or {STUDIO_GHIBLI_PEOPLE_ENDPOINT}. "
                f"Got the following URL instead: {url}"
            )

        mock_response = json.loads(fake_response_data.read())

        return self.build_fake_response(url, mock_response)
