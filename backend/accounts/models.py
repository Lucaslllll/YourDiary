from django.db import models
from django.utils import timezone



class User(models.Model):
	username = models.CharField(max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(null=True, blank=True)
	password = models.CharField(max_length=100)
	image = models.ImageField(upload_to="images/profile", null=True, blank=True)
	terms_of_use = models.BooleanField(default=True)

	def __str__(self):
		return self.username


class Message(models.Model):
	text = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')
	seen = models.BooleanField(default='False')

	def __str__(self):
		return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)



class CodeManager(models.Manager):

    def get_queryset(self):
        super().get_queryset().filter(
            created__lt=timezone.now()-timezone.timedelta(minutes=15)
        ).delete()
        return super().get_queryset().filter(
            created__gte=timezone.now()-timezone.timedelta(minutes=15)
        )


class Code(models.Model):
    value = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(default=timezone.now)

    objects = CodeManager()
