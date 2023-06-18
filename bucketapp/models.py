from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.safestring import mark_safe

# Create your models here.

class Bucket(models.Model):

    title       = models.CharField(max_length=100)
    description = models.TextField()
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('bucket-detail', kwargs={'pk': self.pk})


class Task(models.Model):

    title       = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    bucket      = models.ForeignKey(Bucket, on_delete=models.CASCADE, related_name='tasks')
    assignee    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complete    = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('bucket-detail', kwargs={'pk': self.bucket.pk})
    
    @property
    def formatted_description(self):
        return mark_safe(markdown.markdown(self.description))