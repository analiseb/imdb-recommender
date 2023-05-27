from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class MoviesListUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # new
    title = models.CharField(max_length=50)
    popularity = models.FloatField()
    vote_average = models.FloatField()
    url_image = models.TextField(null=True,blank=True)

    # class Meta:
    #     unique_together = ('user', 'title',)