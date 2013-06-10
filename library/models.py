from django.db import models

# Create your models here.
class Books(models.Model):
	book_id = models.IntegerField()
	book_name = models.CharField(max_length=50)
	count = models.IntegerField()
	author = models.CharField(max_length=50)
	def __unicode__(self):
		return self.book_name
	

class Students(models.Model):
	s_id = models.CharField(max_length=4)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	def __unicode__(self):
		return self.name

class BookIssued(models.Model):
	b_id = models.ForeignKey(Books)
	s_id = models.ForeignKey(Students)
	def __unicode__(self):
		return str(self.b_id)	
