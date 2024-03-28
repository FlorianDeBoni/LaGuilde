from django.urls import path
from .views import view_index

urlpatterns = [
    path('', view_index.index, name='main'),
    path('url2', view_index.index2, name='main2'),
]
