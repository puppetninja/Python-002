from django.db import models


class Phones(models.Model):
    id = models.IntegerField(primary_key=True)
    phone_name = models.CharField(max_length=1024)
    phone_url = models.CharField(max_length=1024)

    class Meta:
        db_table = 'phones'


class PhonesWithOpinions(models.Model):
    id = models.IntegerField(primary_key=True)
    phone_name = models.CharField(max_length=1024)
    positive = models.FloatField()
    negative = models.FloatField()

    class Meta:
        db_table = 'phone_opinions'


class PhoneComments(models.Model):
    id = models.IntegerField(primary_key=True)
    phone_name = models.CharField(max_length=1024)
    comment_content = models.TextField()
    comment_date = models.DateField()

    class Meta:
        db_table = 'phone_comments_cleansed'
