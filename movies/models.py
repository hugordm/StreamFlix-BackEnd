"""
MOVIES/MODELS.PY - Modelo de Filme

PESSOA 1 EXPLICA:
- Define estrutura da tabela no banco
- Cada campo vira uma coluna
- nota_media é calculada automaticamente
"""

from django.db import models

class Movie(models.Model):
    """
    Modelo de Filme
    """
    
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título"
    )
    
    ano = models.IntegerField(
        verbose_name="Ano"
    )
    
    genero = models.CharField(
        max_length=100,
        verbose_name="Gênero"
    )
    
    sinopse = models.TextField(
        verbose_name="Sinopse"
    )
    
    poster = models.TextField(
        verbose_name="Poster"
    )
    
    backdrop = models.TextField(
        verbose_name="Backdrop",
        blank=True
    )
    
    elenco = models.JSONField(
        default=list,
        verbose_name="Elenco"
    )
    
    trailer = models.URLField(
        blank=True,
        verbose_name="Trailer"
    )
    
    nota_media = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        verbose_name="Nota Média"
    )
    
    duracao = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Duração (min)"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )
    
    class Meta:
        verbose_name = "Filme"
        verbose_name_plural = "Filmes"
        ordering = ['-ano', 'titulo']
        indexes = [
            models.Index(fields=['titulo']),
            models.Index(fields=['genero']),
            models.Index(fields=['ano']),
        ]
    
    def __str__(self):
        return f"{self.titulo} ({self.ano})"
    
    def total_avaliacoes(self):
        return self.reviews.count()
    
    def atualizar_nota_media(self):
        from django.db.models import Avg
        media = self.reviews.aggregate(Avg('nota'))['nota__avg']
        self.nota_media = media if media else 0.0
        self.save()