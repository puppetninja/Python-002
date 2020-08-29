from django.db import models

# Create your models here.
class Review(models.Model):
    # id 自动创建
    review_rating = models.CharField(max_length=5)
    review_content = models.CharField(max_length=50)
