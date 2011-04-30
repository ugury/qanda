from django.db import models
from django.contrib.auth.models import User
import datetime

class Category(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/category/%s" % self.slug
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

class Question(models.Model):
    STATUS = (
              ('0','Draft'),
              ('1','Active')
              )
    title = models.CharField(max_length=120)
    body = models.TextField()
    user = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    pub_date = models.DateField(default=datetime.datetime.now)
    categories = models.ManyToManyField(Category)
    active = models.IntegerField(choices=STATUS)

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/question/%d/%s" % (self.pk,self.slug)
    
    class Meta:
        ordering = ['-pub_date']


class Answer(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    pub_date = models.DateField(default=datetime.datetime.now)
    question = models.ForeignKey(Question)
    
    def __unicode__(self):
        return self.content
    
    class Meta:
        ordering = ['-pub_date']
