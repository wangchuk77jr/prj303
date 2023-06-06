from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Music(models.Model):
    HAPPY = 'happy'
    SAD = 'sad'
    DISGUST = 'disgust'
    ANGRY = 'angry'
    SURPRISE = 'surprise'
    NEUTRAL = 'neutral'
    FEAR = 'fear'
    CATEGORY_CHOICES = [
        (HAPPY, 'Happy'),
        (SAD, 'Sad'),
        (DISGUST, 'Disgust'),
        (ANGRY, 'Angry'),
        (SURPRISE, 'Surprise'),
        (NEUTRAL, 'Neutral'),
        (FEAR, 'Fear'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songTitle = models.CharField(max_length=255)
    singer = models.CharField(max_length=355)
    img = models.ImageField(upload_to='music')
    audio_file = models.FileField(upload_to='music', validators=[FileExtensionValidator(['mp3', 'wav', 'ogg', 'm4a', 'flac', 'aac', 'wma', 'aiff', 'alac', 'opus','mp4'])])
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    

    def __str__(self):
        return self.songTitle
    
def default_avatar():
    return 'default_avatar.png'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', default=default_avatar, blank=True, null=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    token_expiration_time = models.DateTimeField(null=True)
    def __str__(self):
        return self.user.username


