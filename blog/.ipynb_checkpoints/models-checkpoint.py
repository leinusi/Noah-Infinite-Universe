from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings



class Post(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('home', kwargs={'pk': self.pk})

class Imgg(models.Model):
    img_url = models.ImageField(upload_to='photos/%Y%m%d',blank=True,null=True)
    
    
class Chars(models.Model):
     char_url = models.ImageField(upload_to='templates/%Y%m%d',blank=True,null=True)
        
class UserGeneratedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=500)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + str(self.generated_at)
    
class ViewImage(models.Model):
    username = models.CharField(max_length=255)
    image_id = models.CharField(max_length=255, unique=True)

    @property
    def image_file_path(self):
        return f"/media/temps/{self.username}/{self.image_id}.png"