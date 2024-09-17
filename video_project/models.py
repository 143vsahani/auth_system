from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    subtitle_file = models.FileField(upload_to='subtitles/', blank=True, null=True)  # This will store extracted subtitles
    upload_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50, default='en')  # Subtitle language, default to 'en' for English
    #uploaded_at = models.DateTimeField(auto_now_add=True)

class Subtitle(models.Model):
    video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    subtitle_file = models.FileField(upload_to='subtitles/')



    def __str__(self):
        return self.title
    
