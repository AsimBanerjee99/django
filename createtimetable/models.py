from django.db import models
from django.contrib.auth.models import User
import json


# Create your models here.


class rowName(models.Model):

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True)
    
    def __str__(self):
        return self.name + str(self.customer)

class columnName(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    # row_name = models.ForeignKey(rowName, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True)
    
    def __str__(self):
        return self.name + str(self.customer)

class timeTable(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    row_name = models.ForeignKey(rowName, on_delete=models.SET_NULL, blank=True, null=True)
    column_name = models.ForeignKey(columnName, on_delete=models.SET_NULL, blank=True, null=True)
    item = models.CharField(max_length=60, blank=True)
    
    def __str__(self):
        return str(self.customer) + "(" + str(self.row_name) + "+" + str(self.column_name) +")" 

