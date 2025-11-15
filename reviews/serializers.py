"""
EXPLICAÇÃO - PESSOA 2:
Serializers para avaliações

Convertem Review (Python) ←→ JSON (API)
"""

from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer completo de avaliação
    
    Usado para listar e exibir avaliações
    """
    
    # Campos adicionais
    filme_titulo = serializers.CharField(
        source='filme.titulo',
        read_only=True
    )
    
    class Meta:
        model = Review
        fields = [
            'id',            # ID da avaliação
            'usuario',       # Nome do usuário
            'filme',         # ID do filme
            'filme_titulo',  # Título do filme (extra)
            'nota',          # Nota (1-5)
            'comentario',    # Comentário
            'created_at',    # Data
        ]
        read_only_fields = ['id', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criar avaliação
    
    Valida os dados antes de salvar
    """
    
    class Meta:
        model = Review
        fields = ['usuario', 'filme', 'nota', 'comentario']
    
    def validate_nota(self, value):
        """
        Valida se a nota está entre 1 e 5
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Nota deve estar entre 1 e 5")
        return value
    
    def validate_usuario(self, value):
        """
        Valida se o nome do usuário não está vazio
        """
        if not value.strip():
            raise serializers.ValidationError("Nome do usuário é obrigatório")
        return value.strip()