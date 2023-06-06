from django.contrib import admin
from .models import Music
from .models import Profile

class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin.css',),
        }

class MusicAdmin(admin.ModelAdmin):
    list_display = ('songTitle', 'singer', 'category', 'img', 'audio_file','user')

admin.site.register(Music, MusicAdmin)

admin.site.register(Profile)
