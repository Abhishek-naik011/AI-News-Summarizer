from django.db import models

class NewsArticle(models.Model):

    title = models.CharField(max_length=500)

    summary = models.TextField()

    category = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title