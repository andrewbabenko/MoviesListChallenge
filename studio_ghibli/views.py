from django.views import View
from django.shortcuts import render

from studio_ghibli.services import get_films_data


class StudioGhibliView(View):
    """ Handles requests for films data """
    template_name = "index.html"

    def get(self, request):
        """ Get list of all movies from the Studio Ghibli """
        films_data = get_films_data()

        return render(request, self.template_name, {"films": films_data})
