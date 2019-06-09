from django.db import models

# Create your models here.


class PhoneModel(models.Model):

    username  = models.CharField(verbose_name='username',null=True,blank=True, max_length = 2000)
    phone     = models.CharField(verbose_name='phone',null=True,blank=True, max_length = 2000)
