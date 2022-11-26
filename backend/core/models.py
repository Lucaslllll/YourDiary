from django.db import models
from accounts.models import User


class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Annotation(models.Model):
	name = models.CharField(max_length=255)
	text = models.TextField()
	thumb = models.ImageField(null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	category = models.ManyToManyField(Category, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	public = models.BooleanField(default=False)
	edit = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class Like(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	like = models.BooleanField()

class Favorite(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class Reports(models.Model):
	annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	details = models.TextField()

	def __str__(self):
		return self.annotation.name + " | " + self.title