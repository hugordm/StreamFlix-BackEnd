"""
EXPLICAÇÃO - PESSOA 1:
Serializers convertem dados entre Python e JSON

Python (Model) ←→ JSON (API)

Usado para:
1. Transformar filmes do banco em JSON para enviar ao frontend
2. Validar dados que chegam do frontend
"""

from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer completo de filme
    
    Converte um objeto Movie em JSON:
    Movie(titulo="Matrix") → {"titulo": "Matrix", "ano": 1999, ...}
    """
    
    # Campo calculado (não existe no banco)
    total_avaliacoes = serializers.ReadOnlyField()
    
    class Meta:
        model = Movie
        fields = [
            'id',                # ID único do filme
            'titulo',            # Título
            'ano',               # Ano
            'genero',            # Gênero
            'sinopse',           # Sinopse
            'poster',            # Imagem poster
            'backdrop',          # Imagem backdrop
            'elenco',            # Lista de atores
            'trailer',           # Link do trailer
            'nota_media',        # Nota média
            'duracao',           # Duração
            'total_avaliacoes',  # Quantidade de avaliações
            'created_at',        # Data de criação
        ]
        # Campos que não podem ser alterados
        read_only_fields = ['id', 'nota_media', 'created_at']


class MovieListSerializer(serializers.ModelSerializer):
    """
    Serializer resumido para listagem
    
    Retorna menos informações para economizar dados
    Usado na lista de filmes (não nos detalhes)
    """
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'titulo',
            'ano',
            'genero',
            'poster',
            'nota_media',
        ]


class MovieCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar/editar filmes
    
    Valida os dados antes de salvar no banco
    """
    
    class Meta:
        model = Movie
        fields = [
            'titulo',
            'ano',
            'genero',
            'sinopse',
            'poster',
            'backdrop',
            'elenco',
            'trailer',
            'duracao',
        ]
    
    def validate_ano(self, value):
        """
        Valida se o ano é válido
        """
        if value < 1888 or value > 2030:
            raise serializers.ValidationError("Ano inválido")
        return value