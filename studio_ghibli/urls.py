from django.urls import path

from studio_ghibli.views import StudioGhibliView

urlpatterns = [
    path('movies/', StudioGhibliView.as_view(), name='studio_ghibli_movie_list'),
]
