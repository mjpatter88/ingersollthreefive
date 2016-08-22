from django.db import models

class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, null=True)
	phone = models.CharField(max_length=100)
	comments = models.TextField(null=True)
	date = models.DateTimeField(auto_now_add=True)
	waiting_list = models.BooleanField(default=False)

	def __str__(self):
		return "Name: {} Email: {} Date: {}".format(self.name, self.email, self.date)
