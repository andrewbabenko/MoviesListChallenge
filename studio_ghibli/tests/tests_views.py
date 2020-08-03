import json
import mock
from copy import deepcopy

from memcache import Client
from django.http import HttpResponse
from requests.exceptions import HTTPError

from movie_list.settings import (
    STUDIO_GHIBLI_FILMS_ENDPOINT,
    STUDIO_GHIBLI_PEOPLE_ENDPOINT,
    STUDIO_GHIBLI_URL,
    STORE_CACHE_FOR
)
from studio_ghibli.views import StudioGhibliView
from studio_ghibli.tests.conftest import MoviesTestCase, FakeRequest


class StudioGhibliViewsTests(MoviesTestCase):

    @mock.patch("studio_ghibli.views.render")
    @mock.patch("studio_ghibli.views.get_films_data")
    def test_get_view(self, mock_films_data, mock_render):
        """ Test StudioGhibliView GET method behaviour with mocked
        film data extraction function
        """

        films_with_characters_file = open(
            "studio_ghibli/tests/resources/contexts/films_with_characters.json",
            "r"
        )
        films_with_characters_data = json.loads(films_with_characters_file.read())

        response_content = b"fake_data"

        def _fake_render(request, template, context) -> HttpResponse:
            """ Mock of django.shortcuts.render() function

            :param request: received request
            :param template: name of HTML template to be rendered
            :param context: data, that should be rendered on HTML template
            :return: fake response
            """
            expected_template = 'index.html'

            self.assertEqual(context, films_with_characters_data)
            self.assertEqual(template, expected_template)

            return HttpResponse(content=response_content)

        mock_films_data.return_value = deepcopy(films_with_characters_data["films"])
        mock_render.side_effect = _fake_render

        fake_request = FakeRequest()

        view = StudioGhibliView()
        response = view.get(fake_request)

        self.assertEqual(response.content, response_content)

    @mock.patch.object(Client, 'get')
    @mock.patch("studio_ghibli.views.render")
    def test_get_view_data_from_cache(self, mock_render, mock_cache_get):
        """ Test StudioGhibliView GET method behaviour with cached data """

        films_with_characters_file = open(
            "studio_ghibli/tests/resources/contexts/films_with_characters.json",
            "r"
        )
        films_with_characters_data = json.loads(films_with_characters_file.read())

        response_content = b"fake_data"

        def fake_get_cache(key) -> dict:
            """ Mock for cache.get() method

            :param key: cached data search key
            :return: fake cached data
            """
            expected_cache_key = f":1:{STUDIO_GHIBLI_URL}"

            self.assertEqual(key, expected_cache_key)

            return deepcopy(films_with_characters_data["films"])

        mock_cache_get.side_effect = fake_get_cache
        mock_render.return_value = HttpResponse(content=response_content)

        fake_request = FakeRequest()

        view = StudioGhibliView()
        response = view.get(fake_request)

        self.assertEqual(response.content, response_content)

    @mock.patch.object(Client, 'get', return_value=None)
    @mock.patch.object(Client, 'set')
    @mock.patch("studio_ghibli.services.requests.get")
    @mock.patch("studio_ghibli.views.render")
    def test_get_view_composed_data(self, mock_render, mock_requests_get, *args):
        """ Test StudioGhibliView GET method behaviour with composed data """

        response_content = b"fake_data"

        def _fake_api(url):
            """ Check request to external API and return mocked response

            :param url: external API endpoint
            :return: mocked response
            """
            self.assertIn(STUDIO_GHIBLI_URL, url)

            return self.fake_api(url)

        mock_render.return_value = HttpResponse(content=response_content)
        mock_requests_get.side_effect = _fake_api

        fake_request = FakeRequest()

        view = StudioGhibliView()
        response = view.get(fake_request)

        self.assertEqual(response.content, response_content)

    @mock.patch.object(Client, 'get', return_value=None)
    @mock.patch.object(Client, 'set')
    @mock.patch("studio_ghibli.views.render")
    @mock.patch("studio_ghibli.services.requests.get")
    def test_get_view_raise_400_error_for_films(self, mock_requests_get, *args):
        """ Test StudioGhibliView GET method behaviour with error for getting films data """

        def _fake_api(url):
            """ Check request to external API and return mocked response for `films/` endpoint with
            status code 400 to raise error

            :param url: external API endpoint
            :return: mocked response
            """
            self.assertIn(STUDIO_GHIBLI_URL, url)

            return self.build_fake_response(url, {"fake": True}, 400)

        mock_requests_get.side_effect = _fake_api

        fake_request = FakeRequest()

        view = StudioGhibliView()
        with self.assertRaises(HTTPError) as http_error:
            view.get(fake_request)

        expected_exception = (
            "400 Client Error: None for url: "
            f"{STUDIO_GHIBLI_FILMS_ENDPOINT}?limit=250&fields=id,title"
        )
        self.assertEqual(str(http_error.exception), expected_exception)

    @mock.patch.object(Client, 'get', return_value=None)
    @mock.patch.object(Client, 'set')
    @mock.patch("studio_ghibli.views.render")
    @mock.patch("studio_ghibli.services.requests.get")
    def test_get_view_raise_400_error_for_characters(self, mock_requests_get, *args):
        """ Test StudioGhibliView GET method behaviour with error for getting characters data """

        def _fake_api(url):
            """ Check request to external API and return mocked response for `people/` endpoint with
            status code 400 to raise error

            :param url: external API endpoint
            :return: mocked response
            """
            self.assertIn(STUDIO_GHIBLI_URL, url)

            if STUDIO_GHIBLI_PEOPLE_ENDPOINT in url:
                return self.build_fake_response(url, {"fake": True}, 400)

            return self.fake_api(url)

        mock_requests_get.side_effect = _fake_api

        fake_request = FakeRequest()

        view = StudioGhibliView()
        with self.assertRaises(HTTPError) as http_error:
            view.get(fake_request)

        expected_exception = (
            "400 Client Error: None for url: "
            f"{STUDIO_GHIBLI_PEOPLE_ENDPOINT}?limit=250&fields=name,films"
        )
        self.assertEqual(str(http_error.exception), expected_exception)

    @mock.patch.object(Client, 'get', return_value=None)
    @mock.patch.object(Client, 'set')
    @mock.patch("studio_ghibli.views.render")
    @mock.patch("studio_ghibli.services.requests.get")
    def test_get_view_create_cache(self, mock_requests_get, mock_render, mock_cache_set, *args):
        """ Test StudioGhibliView GET method behaviour with setting up cache """

        films_with_characters_file = open(
            "studio_ghibli/tests/resources/contexts/films_with_characters.json",
            "r"
        )
        films_with_characters_data = json.loads(films_with_characters_file.read())

        response_content = b"fake_data"

        def fake_set_cache(key, data, timeout):
            """Mock for cache.set() method

            :param key: cached data search key
            :param data: data to be saved at cache
            :param timeout: data storing period
            """
            expected_cache_key = f":1:{STUDIO_GHIBLI_URL}"

            self.assertEqual(key, expected_cache_key)
            self.assertEqual(data, films_with_characters_data["films"])
            self.assertEqual(timeout, STORE_CACHE_FOR)

        mock_requests_get.side_effect = self.fake_api
        mock_render.return_value = HttpResponse(content=response_content)
        mock_cache_set.side_effect = fake_set_cache

        fake_request = FakeRequest()

        view = StudioGhibliView()
        response = view.get(fake_request)

        self.assertEqual(response.content, response_content)
