from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    date_of_birth = models.DateField()


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='изображение')
    video = models.URLField(max_length=200, blank=True, null=True, verbose_name='ссылка на видео')

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
    
    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', args=[self.id])

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='Текст')
    original_body = models.TextField(verbose_name='Оригинальный текст', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    was_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
    def save(self, *args, **kwargs):
        if self.body != self.original_body:
            self.was_edited = True 
        super().save(*args, **kwargs)


