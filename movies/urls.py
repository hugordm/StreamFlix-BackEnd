"""
EXPLICAÇÃO - PESSOA 1:
Define as rotas do app de filmes

Todas começam com /api/movies/ (definido no config/urls.py)
"""

from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    MovieSearchView,
    MovieByGenreView,
    MovieByYearView,
    MovieCreateView,
)

urlpatterns = [
    # GET /api/movies/
    # Lista todos os filmes
    path('', MovieListView.as_view(), name='movie-list'),
    
    # GET /api/movies/{id}/
    # Detalhes de um filme específico
    # Exemplo: /api/movies/1/
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    
    # GET /api/movies/search/?q=matrix
    # Busca filmes por termo
    path('search/', MovieSearchView.as_view(), name='movie-search'),
    
    # GET /api/movies/genre/Ação/
    # Filtra por gênero
    path('genre/<str:genero>/', MovieByGenreView.as_view(), name='movie-by-genre'),
    
    # GET /api/movies/year/2023/
    # Filtra por ano
    path('year/<int:ano>/', MovieByYearView.as_view(), name='movie-by-year'),
    
    # POST /api/movies/create/
    # Cria novo filme
    path('create/', MovieCreateView.as_view(), name='movie-create'),
]