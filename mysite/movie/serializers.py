from rest_framework import serializers
from .models import (UserProfile, Country, Director,
                     Actor, Genre, Movie,
                     MovieLanguages, Moments, Rating,
                     Favorite, FavoriteMovie, History)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UseProfileSerializers(serializers.ModelSerializer):
    class Meta:
       model = UserProfile
       fields = '__all__'


class UseProfileSimpleSerializers(serializers.ModelSerializer):
    class Meta:
       model = UserProfile
       fields = ['first_name', 'last_name']


class MovieSerializers(serializers.ModelSerializer):
    year = serializers.DateField(format='%d-%m-%Y')
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year', 'avg_rating', 'status_movie']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

class  CountrySerializers(serializers.ModelSerializer):
    class Meta:
       model = Country
       fields = ['id', 'country_name']


class CountryDetailSerializer(serializers.ModelSerializer):
    countries = MovieSerializers(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ['countries']


class  DirectorSerializers(serializers.ModelSerializer):
    class Meta:
       model =  Director
       fields = ['id', 'director_image', 'director_name', 'age']


class DirectorDetailSerializer(serializers.ModelSerializer):
    directors = MovieSerializers(many=True, read_only=True)
    age = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Director
        fields = ['id', 'director_image', 'director_name', 'age', 'bio', 'directors']


class ActorSerializers(serializers.ModelSerializer):
    age = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Actor
        fields = ['id', 'actor_image', 'actor_name', 'age']


class ActorDetailSerializer(serializers.ModelSerializer):
    movies = MovieSerializers(many=True, read_only=True)
    age = serializers.DateField(format='%d-%m-%Y')


    class Meta:
        model = Actor
        fields = ['id', 'actor_image', 'actor_name', 'age', 'bio','movies']


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id','genre_name']


class GenreDetailSerializer(serializers.ModelSerializer):
    movies_genre = MovieSerializers(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'genre_name', 'movies_genre']


class  MovieLanguagesSerializers(serializers.ModelSerializer):
    class Meta:
       model = MovieLanguages
       fields = ['id', 'language']


class  MomentsSerializers(serializers.ModelSerializer):

    class Meta:
       model =  Moments
       fields = ['movie_moments']


class RatingSerializers(serializers.ModelSerializer):
    user = UseProfileSimpleSerializers(read_only=True)


    class Meta:
        model = Rating
        fields = ['id', 'user', 'stars', 'text', 'created_date']


class MovieDetailSerializers(serializers.ModelSerializer):
    country = CountrySerializers(many=True, read_only=True)
    director = DirectorSerializers(many=True, read_only=True)
    actor = ActorSerializers(many=True, read_only=True)
    genre = GenreSerializers(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    moment = MomentsSerializers(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'movie_name', 'year', 'country', 'director',
            'actor', 'genre', 'types', 'movie_time', 'description',
            'movie_trailer', 'movie_image', 'moment', 'status_movie',
            'avg_rating'
        ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()


class FavoriteMovieSerializers(serializers.ModelSerializer):
    movie = MovieSerializers(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),
                                                    write_only=True, source='movie')

    class Meta:
        model = FavoriteMovie
        fields = ['id', 'movie', 'movie_id']


class FavoriteSerializers(serializers.ModelSerializer):
    user = UseProfileSimpleSerializers(read_only=True)
    items = FavoriteMovieSerializers(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'items']


class HistorySerializers(serializers.ModelSerializer):
    movie = MovieSerializers(read_only=True)
    user = UseProfileSimpleSerializers(read_only=True)
    viewed_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)



    class Meta:
        model = History
        fields = ['id', 'user', 'viewed_at', 'movie']

