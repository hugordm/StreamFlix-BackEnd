"""
EXPLICAÇÃO - PESSOA 2:
Define as rotas do app de avaliações

Todas começam com /api/reviews/
"""

from django.urls import path
from .views import (
    ReviewListView,
    ReviewCreateView,
    MovieReviewsView,
    ReviewDetailView,
    ReviewDeleteView,
)

urlpatterns = [
    # GET /api/reviews/
    # Lista todas as avaliações
    path('', ReviewListView.as_view(), name='review-list'),
    
    # POST /api/reviews/create/
    # Cria nova avaliação
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    
    # GET /api/reviews/movie/{movie_id}/
    # Lista avaliações de um filme específico
    # Exemplo: /api/reviews/movie/1/
    path('movie/<int:movie_id>/', MovieReviewsView.as_view(), name='movie-reviews'),
    
    # GET /api/reviews/{id}/
    # Detalhes de uma avaliação
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    
    # DELETE /api/reviews/{id}/
    # Deleta uma avaliação
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]