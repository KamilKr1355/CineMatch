from django.urls import path
from .views import GraphDataView, MovieListView

urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('graph/', GraphDataView.as_view(), name='graph-data'),
]