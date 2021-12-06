from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.urls import reverse
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.files.storage import FileSystemStorage


class Ip(models.Model):
    ip = models.CharField(max_length=50)


class Post(models.Model):
    GENDER = (('male', 'male'),  ('female', 'female'))
    name = models.CharField(max_length=30)
    image = models.ImageField()
    description = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=11, choices=GENDER, default='male')
    likes = models.ManyToManyField(Ip, related_name="likes", blank=True)
    dislikes = models.ManyToManyField(Ip, related_name="dislikes", blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class Dislikes(models.Model):
    user = models.ForeignKey(Ip, on_delete=models.CASCADE, related_name='user_dislike')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_dislike')


class Likes(models.Model):
    user = models.ForeignKey(Ip, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

