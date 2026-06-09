from django.urls import path
from .views import (
    PersonalizedRecommendationView,
    ShortestPathView,
    ActorRankingView,
    CommonElementsView,
    TimelineView,
    GenreStatsView,
    SixDegreesQuizView,
)

urlpatterns = [
    path('path/', ShortestPathView.as_view(), name='shortest-path'),
    path('personalized/', PersonalizedRecommendationView.as_view(), name='personalized'),
    path('ranking/', ActorRankingView.as_view(), name='actor-ranking'),
    path('common/', CommonElementsView.as_view(), name='common-elements'),
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('genres/', GenreStatsView.as_view(), name='genre-stats'),
    path('quiz/', SixDegreesQuizView.as_view(), name='six-degrees-quiz'),
]