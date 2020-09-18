from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=40)
    course_instructor = models.CharField(max_length=50, default="")
    course_code = models.CharField(max_length=50)
    details = models.TextField()
    rating = models.IntegerField(default = 0)
    course_likes = models.ManyToManyField(User, related_name='likes', blank = True)
    course_dislikes = models.ManyToManyField(User, related_name='dislikes', blank = True)

    def __str__(self):
        return self.course_name 

    def get_absolute_url(self):
        return reverse('courses_detail', kwargs = {'pk' : self.pk})

class Reviews(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    course_rating=models.IntegerField(default = 0)
    course_review=models.CharField(max_length=150,null=True,blank=True)
    course_rater=models.ForeignKey(User,related_name="reviewer",on_delete=models.CASCADE)
    review_likes = models.ManyToManyField(User, related_name="review_likes", blank=True)
    review_dislikes = models.ManyToManyField(User, related_name="review_dislikes", blank = True)
    

