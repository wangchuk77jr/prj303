from django.db import models

class Feedback(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.email}: {self.message}"
