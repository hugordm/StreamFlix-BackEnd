"""
EXPLICAÇÃO - PESSOA 2:
Configuração do painel admin para avaliações
"""

from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Como as avaliações aparecem no admin
    """
    
    # Colunas exibidas
    list_display = [
        'usuario',      # Nome do usuário
        'filme',        # Filme avaliado
        'nota',         # Nota (1-5)
        'created_at'    # Data
    ]
    
    # Filtros laterais
    list_filter = ['nota', 'created_at']
    
    # Campo de busca
    search_fields = ['usuario', 'filme__titulo', 'comentario']
    
    # Ordenação padrão
    ordering = ['-created_at']
    
    # Campos não editáveis
    readonly_fields = ['created_at']