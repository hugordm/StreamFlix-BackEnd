"""
EXPLICAÇÃO - PESSOA 2:
Views para gerenciar avaliações
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from movies.models import Movie


class ReviewListView(generics.ListAPIView):
    """
    GET /api/reviews/
    
    Lista TODAS as avaliações do sistema
    
    EXPLICAÇÃO:
    - Busca todas as reviews
    - Paginação automática
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreateView(generics.CreateAPIView):
    """
    POST /api/reviews/
    
    Cria uma nova avaliação
    
    EXPLICAÇÃO:
    - Recebe JSON com: usuario, filme, nota, comentario
    - Valida os dados
    - Salva no banco
    - Atualiza nota média do filme automaticamente
    
    Exemplo de body:
    {
        "usuario": "João Silva",
        "filme": 1,
        "nota": 5,
        "comentario": "Filme incrível!"
    }
    """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método create para retornar mensagem customizada
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Salva a avaliação
        review = serializer.save()
        
        return Response({
            'message': 'Avaliação criada com sucesso!',
            'review': ReviewSerializer(review).data
        }, status=status.HTTP_201_CREATED)


class MovieReviewsView(APIView):
    """
    GET /api/reviews/movie/{movie_id}/
    
    Lista todas as avaliações de UM filme específico
    
    EXPLICAÇÃO:
    - Recebe ID do filme na URL
    - Busca todas as reviews desse filme
    - Retorna ordenado por mais recente
    """
    
    def get(self, request, movie_id):
        # Busca o filme (retorna 404 se não existir)
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Busca todas as reviews desse filme
        reviews = Review.objects.filter(filme=movie)
        
        # Serializa
        serializer = ReviewSerializer(reviews, many=True)
        
        return Response({
            'filme': movie.titulo,
            'nota_media': movie.nota_media,
            'total_avaliacoes': reviews.count(),
            'avaliacoes': serializer.data
        })


class ReviewDetailView(generics.RetrieveAPIView):
    """
    GET /api/reviews/{id}/
    
    Detalhes de uma avaliação específica
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/reviews/{id}/
    
    Deleta uma avaliação
    
    EXPLICAÇÃO:
    - Recebe ID da avaliação
    - Deleta do banco
    - Recalcula nota média do filme automaticamente
    """
    queryset = Review.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        filme = review.filme
        
        # Deleta a review
        self.perform_destroy(review)
        
        # Recalcula nota média do filme
        filme.atualizar_nota_media()
        
        return Response({
            'message': 'Avaliação deletada com sucesso!'
        }, status=status.HTTP_200_OK)