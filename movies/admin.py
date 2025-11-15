"""
EXPLICAÇÃO - PESSOA 1:
Configuração do painel administrativo

Django Admin = interface web automática para gerenciar dados
Acesse em: http://localhost:8000/admin/
"""

from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Como os filmes aparecem no admin
    """
    
    # Colunas exibidas na lista
    list_display = [
        'titulo',           # Título
        'ano',              # Ano
        'genero',           # Gênero
        'nota_media',       # Nota
        'total_avaliacoes'  # Qtd avaliações
    ]
    
    # Filtros laterais
    list_filter = ['genero', 'ano']
    
    # Campo de busca
    search_fields = ['titulo', 'sinopse']
    
    # Ordenação padrão
    ordering = ['-ano', 'titulo']