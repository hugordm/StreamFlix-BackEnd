"""
EXPLICAÇÃO - PESSOA 1:
Views processam as requisições HTTP

Fluxo:
1. Frontend faz requisição (GET /api/movies/)
2. Django direciona para a view correta
3. View busca dados no banco
4. View retorna JSON
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Movie
from .serializers import MovieSerializer, MovieListSerializer, MovieCreateSerializer


class MovieListView(generics.ListAPIView):
    """
    GET /api/movies/
    
    Lista todos os filmes com paginação automática
    
    EXPLICAÇÃO:
    - queryset: define quais filmes buscar (todos)
    - serializer_class: define como converter em JSON
    - DRF faz tudo automaticamente (paginação, JSON, etc)
    """
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


class MovieDetailView(generics.RetrieveAPIView):
    """
    GET /api/movies/{id}/
    
    Retorna detalhes completos de UM filme
    
    EXPLICAÇÃO:
    - O {id} vem da URL
    - Django busca o filme automaticamente
    - Retorna com todas as informações
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieSearchView(APIView):
    """
    GET /api/movies/search/?q=matrix
    
    Busca filmes por título ou sinopse
    
    EXPLICAÇÃO:
    - Pega o parâmetro 'q' da URL (?q=matrix)
    - Busca no título E na sinopse
    - Retorna lista de filmes encontrados
    """
    
    def get(self, request):
        # Pega o termo de busca da URL
        query = request.GET.get('q', '').strip()
        
        # Se não tem nada, retorna erro
        if not query:
            return Response({
                'error': 'Parâmetro "q" é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Busca filmes (case-insensitive)
        # Q permite fazer OR (OU) entre condições
        # icontains = "contém" (ignora maiúsculas/minúsculas)
        movies = Movie.objects.filter(
            Q(titulo__icontains=query) | Q(sinopse__icontains=query)
        )
        
        # Serializa os resultados
        serializer = MovieListSerializer(movies, many=True)
        
        return Response({
            'count': movies.count(),
            'results': serializer.data
        })


class MovieByGenreView(APIView):
    """
    GET /api/movies/genre/{genero}/
    
    Filtra filmes por gênero
    Exemplo: /api/movies/genre/Ação/
    
    EXPLICAÇÃO:
    - {genero} vem da URL
    - Busca todos os filmes desse gênero
    """
    
    def get(self, request, genero):
        # Busca filmes (case-insensitive)
        movies = Movie.objects.filter(genero__iexact=genero)
        
        # Se não encontrou nenhum
        if not movies.exists():
            return Response({
                'error': f'Nenhum filme encontrado no gênero "{genero}"'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieListSerializer(movies, many=True)
        
        return Response({
            'genero': genero,
            'count': movies.count(),
            'results': serializer.data
        })


class MovieByYearView(APIView):
    """
    GET /api/movies/year/{ano}/
    
    Filtra filmes por ano
    Exemplo: /api/movies/year/2023/
    """
    
    def get(self, request, ano):
        # Tenta converter ano para número
        try:
            ano = int(ano)
        except ValueError:
            return Response({
                'error': 'Ano inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Busca filmes desse ano
        movies = Movie.objects.filter(ano=ano)
        
        if not movies.exists():
            return Response({
                'error': f'Nenhum filme encontrado no ano {ano}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieListSerializer(movies, many=True)
        
        return Response({
            'ano': ano,
            'count': movies.count(),
            'results': serializer.data
        })


class MovieCreateView(generics.CreateAPIView):
    """
    POST /api/movies/
    
    Cria um novo filme
    
    EXPLICAÇÃO:
    - Recebe dados JSON do frontend
    - Valida usando o serializer
    - Salva no banco
    """
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer