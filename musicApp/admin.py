from django.contrib import admin
from .models import Feedback

# Register your models here.
class MyModelAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin.css',),
        }
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email','message')

admin.site.register(Feedback,FeedbackAdmin)

admin.site.site_header = "Emovibe Music Administration"