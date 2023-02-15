from django.db import models
from accounts.models import User


class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Annotation(models.Model):
	name = models.CharField(max_length=255)
	preview = models.CharField(max_length=255, null=True)
	text = models.TextField()
	thumb = models.ImageField(upload_to="images/annotations", null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	category = models.ManyToManyField(Category, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	public = models.BooleanField(default=False)
	edit = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ['-id']

class Like(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


# Favorite e Profile são problemas iguais
# Mas em favorite vou fazer a moda antiga
# Sem o manytomanyfield do django
class Favorite(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True, null=True)


class Report(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=255)
	details = models.TextField()

	def __str__(self):
		return self.title

class Comment(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
