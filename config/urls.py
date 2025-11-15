"""
URLs PRINCIPAIS

Conecta endereços web aos apps:
- /admin/ → Painel administrativo
- /api/movies/ → App de filmes
- /api/reviews/ → App de avaliações
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/movies/', include('movies.urls')),
    path('api/reviews/', include('reviews.urls')),
]