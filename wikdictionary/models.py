from django.db import models

# Create your models here.
class Dict(models.Model):
    word = models.TextField(primary_key=True)
    autoSugg = models.TextField()
    Defi = models.TextField()
    freq = models.IntegerField()

    class Meta:
        db_table = "Dict"

class DictMap(models.Model):
    word = models.TextField(primary_key=True)
    origin = models.TextField()

    class Meta:
        db_table = "DictMap"
