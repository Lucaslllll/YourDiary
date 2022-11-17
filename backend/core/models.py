from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(null=True, blank=True)
	password = models.CharField(max_length=100)

	def __str__(self):
		return self.username

class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Annotation(models.Model):
	name = models.CharField(max_length=255)
	text = models.TextField()
	thumb = models.ImageField(null=True, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	category = models.ManyToManyField(Category, on_delete=models.CASCADE, null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	public = models.BooleanField(default=False)

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

	return self.annotation.name + " | " + self.title