from django.urls import path
from . import views
from .views import music_search
urlpatterns = [
    path('',views.Home,name='home'),
    path('Face-expression-detection/',views.FaceDetection,name='face-expression'),
    path('recomended-music/',views.MusicPlay,name='music-play'),
    path('music/search/', music_search, name='music_search'),
]
