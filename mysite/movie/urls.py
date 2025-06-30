from django.urls import path, include

from .views import (UserProfileViewSet, RatingViewSet,
                    FavoriteViewSet, FavoriteMovieViewSet,
                    RegisterView, CustomLoginView, LogoutView,
                    MovieListAPIView, MovieDetailListAPIView,
                    MomentsListAPIView, MovieLanguagesListAPIView,
                    CountryListAPIView, CountryDetailListAPIView,
                    ActorListAPIView, ActorDetailListAPIView,
                    DirectorListAPIView, DirectorDetailListAPIView,
                    GenreListAPIView, GenreDetailListAPIView,
                    HistoryListAPIView)

from rest_framework import routers

router = routers.SimpleRouter()

router.register(r'user', UserProfileViewSet, basename='users')
router.register(r'rating', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('movie/', MovieListAPIView.as_view()),
    path('movie/<int:pk>/', MovieDetailListAPIView.as_view()),
    path('actor/', ActorListAPIView.as_view()),
    path('actor/<int:pk>/', ActorDetailListAPIView.as_view()),
    path('director/', DirectorListAPIView.as_view()),
    path('director/<int:pk>/', DirectorDetailListAPIView.as_view()),
    path('country/', CountryListAPIView.as_view()),
    path('country/<int:pk>/', CountryDetailListAPIView.as_view()),
    path('genre/', GenreListAPIView.as_view()),
    path('genre/<int:pk>/', GenreDetailListAPIView.as_view()),
    path('moment/', MomentsListAPIView.as_view()),
    path('language/', MovieLanguagesListAPIView.as_view()),
    path('history/', HistoryListAPIView.as_view()),
    path('favorite/', FavoriteViewSet.as_view(), name='favorite_detail'),
    path('favorite_movie/', FavoriteMovieViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('favorite_movie/<int:pk>/', FavoriteMovieViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]
