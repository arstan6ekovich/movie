from .models import Director, Actor, Genre, Movie
from modeltranslation.translator import TranslationOptions, register

@register(Director)
class DirectorTranslationOptions(TranslationOptions):
    fields = ('director_name', 'bio')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('actor_name', 'bio')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('movie_name',)
