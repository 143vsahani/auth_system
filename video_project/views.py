import subprocess
import os
import re
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import VideoUploadForm
from .models import Video
from .tasks import process_video  # Import the Celery task correctly
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.exceptions import ValidationError



@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                video = form.save()
                # Process the video in the background using the Celery task
                process_video.delay(video.id)
                # Add a success message
                messages.success(request, "Video successfully uploaded and is being processed.")
                return redirect(reverse('list_videos'))  # Redirect to the list of videos after upload
            except ValidationError as e:
                # Handle form validation errors
                messages.error(request, f"Form validation error: {e}")
            except Exception as e:
                # Handle other exceptions
                messages.error(request, f"An unexpected error occurred: {e}")
    else:
        form = VideoUploadForm()
    
    return render(request, 'video_project/upload.html', {'form': form})

def list_videos(request):
    videos = Video.objects.all().order_by('-upload_date')
    return render(request, 'video_project/video_list.html', {'videos': videos})
def process_video(video):
    # Placeholder function to extract subtitles
    subtitle_file_path = f"subtitles/{video.title}_subs.srt"
    
    # You can use ffmpeg or a library to extract subtitles from the video file
    command = f"ffmpeg -i {video.video_file.path} -map 0:s:0 {subtitle_file_path}"
    subprocess.run(command, shell=True)
    
    # Save the generated subtitle file to the Video model
    video.subtitle_file = subtitle_file_path
    video.save()


@login_required
def search_in_video(request, video_id):
    query = request.GET.get('q', '')  # Get the search query parameter
    video = get_object_or_404(Video, id=video_id)  # Get the video by ID
    timestamps = []

    if query:
        # Ensure case-insensitive search
        query = query.lower()
        
        try:
            with open(video.subtitle_file.path, 'r') as f:
                content = f.read()
                
                # Regular expression to find all timestamps
                matches = re.finditer(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', content)
                
                for match in matches:
                    start_time = match.group(1)
                    end_time = match.group(2)
                    
                    # Search for the query within the subtitle content
                    if query in content[match.start():match.end()]:
                        timestamps.append({
                            'start_time': start_time,
                            'end_time': end_time,
                            'line': content[match.end():content.find('\n\n', match.end())]
                        })
        except FileNotFoundError:
            timestamps = []

    return render(request, 'video_project/search_results.html', {'video': video, 'timestamps': timestamps, 'query': query})
@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete()
        return redirect('list_videos')
    return render(request, 'video_project/confirm_delete.html', {'video': video})

def home(request):
    return render(request, 'home.html')
