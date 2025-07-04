from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.utils.text import slugify
from django.urls import reverse
import uuid


def user_dirctory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
	title =models.CharField(max_length=100, verbose_name='Tag')
	slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

	class Meta:
		verbose_name = 'Tags'
		verbose_name_plural = 'Tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])

	def __str__(self):
		return self.title

	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug - slugify(self.slug)
		return super().save(*args, **kwargs)

#this is the post model that creates the post table

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.FileField(upload_to=user_dirctory_path, blank=True, null=True)
    picture = models.ImageField(upload_to=user_dirctory_path, verbose_name="Picture")
    caption = models.CharField(max_length=10000, verbose_name="Caption")
    posted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name="posts")  # Use string reference if Tag is below or imported
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])

    def __str__(self):
        return str(self.caption)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')        
    
