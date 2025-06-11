from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.db.models import Avg

STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
)


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(75)],
                                           null=True, default=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default='simple')
    avatar = models.ImageField(upload_to='user_avatar/', null=True, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Country(models.Model):
   country_name = models.CharField(max_length=64, unique=True)

   def __str__(self):
       return self.country_name

class Director(models.Model):
    director_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.DateField()
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.DateField()
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name

class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='countries')
    director = models.ManyToManyField(Director, related_name='directors')
    actor = models.ManyToManyField(Actor, related_name='movies')
    genre = models.ManyToManyField(Genre, related_name='movies_genre')
    TYPE_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    types = MultiSelectField(choices=TYPE_CHOICES,  max_choices=5)
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.URLField()
    movie_image = models.ImageField(upload_to='movie_images/')
    status_movie = models.CharField(choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.movie_name}'

    def get_avg_rating(self):
        avg = self.rating_set.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 1) if avg else 0


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='movie_videos/', null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.language}, {self.movie}'


class Moments(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='moment')
  movie_moments = models.ImageField(upload_to='movie_moment')

  def __str__(self):
      return f'{self.movie}'

class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 11)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteMovie(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movie}'


class History(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.movie}'


