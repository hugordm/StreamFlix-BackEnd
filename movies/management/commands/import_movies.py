"""
IMPORT_MOVIES.PY - Script para importar filmes do JSON

COMPATÍVEL COM FORMATO EM INGLÊS E PORTUGUÊS!
"""

import json
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Importa filmes do arquivo movies.json'
    
    def handle(self, *args, **options):
        file_path = 'movies.json'
        
        try:
            self.stdout.write('📂 Lendo arquivo movies.json...')
            with open(file_path, 'r', encoding='utf-8') as f:
                movies_data = json.load(f)
            
            created = 0
            updated = 0
            errors = 0
            
            for movie_data in movies_data:
                try:
                    # Compatível com formato em INGLÊS ou PORTUGUÊS
                    titulo = movie_data.get('title') or movie_data.get('titulo')
                    ano = movie_data.get('year') or movie_data.get('ano') or movie_data.get('Ano')
                    genero = movie_data.get('genre') or movie_data.get('genero') or movie_data.get('Gênero')
                    sinopse = movie_data.get('synopsis') or movie_data.get('sinopse')
                    elenco = movie_data.get('cast') or movie_data.get('elenco', [])
                    trailer = movie_data.get('trailer') or movie_data.get('Trailer', '')
                    
                    if not titulo or not ano:
                        errors += 1
                        self.stdout.write(
                            self.style.ERROR(f'  ✗ Filme sem título ou ano')
                        )
                        continue
                    
                    movie, was_created = Movie.objects.update_or_create(
                        titulo=titulo,
                        ano=ano,
                        defaults={
                            'genero': genero or 'Desconhecido',
                            'sinopse': sinopse or '',
                            'poster': movie_data.get('poster', ''),
                            'backdrop': movie_data.get('backdrop', ''),
                            'elenco': elenco,
                            'trailer': trailer,
                            'duracao': movie_data.get('duracao'),
                        }
                    )
                    
                    if was_created:
                        created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'  ✓ Criado: {movie.titulo} ({movie.ano})')
                        )
                    else:
                        updated += 1
                        self.stdout.write(
                            self.style.WARNING(f'  ↻ Atualizado: {movie.titulo} ({movie.ano})')
                        )
                
                except Exception as e:
                    errors += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ Erro: {str(e)}')
                    )
            
            # Mensagem final
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Importação concluída!'
                    f'\n   📊 {created} filmes criados'
                    f'\n   🔄 {updated} filmes atualizados'
                    f'\n   ❌ {errors} erros'
                    f'\n   📁 Total: {Movie.objects.count()} filmes no banco'
                )
            )
            
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('❌ Arquivo movies.json não encontrado na raiz do projeto!')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR('❌ Erro ao ler JSON. Verifique o formato do arquivo.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {str(e)}')
            )