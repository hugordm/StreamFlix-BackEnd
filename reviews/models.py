"""
REVIEWS/MODELS.PY - Modelo de Avaliação

PESSOA 2 EXPLICA:
- Review relaciona usuário com filme
- ForeignKey cria relacionamento Many-to-One
- Quando salva, atualiza nota média do filme
"""

from django.db import models
from movies.models import Movie

class Review(models.Model):
    """
    Modelo de Avaliação de Filme
    """
    
    usuario = models.CharField(
        max_length=100,
        verbose_name="Usuário"
    )
    
    filme = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Filme"
    )
    
    nota = models.IntegerField(
        choices=[
            (1, '⭐ 1 estrela'),
            (2, '⭐⭐ 2 estrelas'),
            (3, '⭐⭐⭐ 3 estrelas'),
            (4, '⭐⭐⭐⭐ 4 estrelas'),
            (5, '⭐⭐⭐⭐⭐ 5 estrelas'),
        ],
        verbose_name="Nota"
    )
    
    comentario = models.TextField(
        blank=True,
        verbose_name="Comentário"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.usuario} - {self.filme.titulo} ({self.nota}⭐)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.filme.atualizar_nota_media()