# video_app/urls.py

from django.urls import path
from . import views
from .views import upload_video, list_videos, home


urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),  # Upload video view
    path('', home, name='home'),  # Home page URL pattern
    path('videos/', views.list_videos, name='list_videos'),    # List uploaded videos
    path('search/<int:video_id>/', views.search_in_video, name='search_in_video'),  # Search subtitles
    path('delete/<int:video_id>/', views.delete_video, name='delete_video'),  # Delete URL pattern
   # path('accounts/', include('accounts.urls')),



]
