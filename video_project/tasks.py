from celery import shared_task
from .models import Video
import subprocess
import os

@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(id=video_id)
        
        # Define the directory for saving subtitles
        subtitle_dir = os.path.join('subtitles')
        
        # Create the directory if it doesn't exist
        if not os.path.exists(subtitle_dir):
            os.makedirs(subtitle_dir)
        
        # Safely construct the subtitle file path
        subtitle_file_path = os.path.join(subtitle_dir, f"{video.title}_subs.srt")
        
        # Construct the ffmpeg command
        command = [
            'ffmpeg', '-i', video.video_file.path, '-map', '0:s:0', subtitle_file_path
        ]
        
        # Run the ffmpeg command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error processing video {video_id}: {result.stderr}")
            return
        
        # Save the generated subtitle file path to the Video model
        video.subtitle_file = subtitle_file_path
        video.save()
    
    except Video.DoesNotExist:
        print(f"Video with ID {video_id} does not exist.")
    
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
