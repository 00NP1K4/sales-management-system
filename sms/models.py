from django.db import models
import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    

    class Meta:
        verbose_name = ("category")
        verbose_name_plural = ("categories")

    def __str__(self):
        return self.name.upper()

class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=False, null=True)
    time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.item_name.upper()

class Issue(models.Model):
    stock =  models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True)
    issue_quantity = models.IntegerField(default='0', blank=False)
    issue_to = models.CharField(max_length=50, blank=True)
    time = models.DateField(default=datetime.date.today)

class Receive(models.Model):
    stock =  models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True)
    receive_quantity = models.IntegerField(default='0', blank=False)
    receive_from = models.CharField(max_length=50, blank=True)
    time = models.DateField(default=datetime.date.today)