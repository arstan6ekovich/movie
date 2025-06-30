
from .models import (UserProfile, Country, Director,
                     Actor, Genre, Movie,
                     MovieLanguages, Moments, Rating,
                     Favorite, FavoriteMovie, History)

from .serializers import (UserSerializer, UseProfileSerializers,
                     MovieDetailSerializers, MovieSerializers,
                     CountrySerializers, CountryDetailSerializer,
                     DirectorSerializers, DirectorDetailSerializer,
                     ActorSerializers, ActorDetailSerializer,
                     GenreSerializers, GenreDetailSerializer,
                     MovieLanguagesSerializers, MomentsSerializers,
                     RatingSerializers, FavoriteSerializers,
                     FavoriteMovieSerializers, HistorySerializers,
                     LoginSerializer)

from rest_framework import viewsets, generics, status, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CheckRating, CheckStatus


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = None
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UseProfileSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class  CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializers


class  CountryDetailListAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer


class  DirectorListAPIView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializers


class  DirectorDetailListAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializer


class  ActorListAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers


class  ActorDetailListAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


class  GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class  GenreDetailListAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer


class  MovieListAPIView(generics.ListAPIView):
    from .filters import MovieFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['movie_name']
    ordering_fields = ['year', 'movie_time']
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers


class MovieDetailListAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializers
    # permission_classes = [CheckStatus]


class  MovieLanguagesListAPIView(generics.ListAPIView):
    queryset = MovieLanguages.objects.all()
    serializer_class = MovieLanguagesSerializers


class  MomentsListAPIView(generics.ListAPIView):
    queryset = Moments.objects.all()
    serializer_class = MomentsSerializers


class  RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    permission_classes = [permissions.IsAuthenticated,CheckRating]


class FavoriteViewSet(generics.RetrieveAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        like, created = Favorite.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(like)
        return Response(serializer.data)


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializers

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return FavoriteMovie.objects.none()
        return FavoriteMovie.objects.filter(favorite__user=user)

    def perform_create(self, serializer):
        like, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer.save(favorite=like)


class  HistoryListAPIView(generics.RetrieveAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializers
