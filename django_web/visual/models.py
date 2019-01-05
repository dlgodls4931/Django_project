from django.db import models
from datetime import datetime

# Create your models here.
class Board(models.Model):
    idx=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=2000) 
    writer=models.CharField(max_length=2000) 
    writedate=models.DateTimeField(default=datetime.now,blank=True)
    hit=models.IntegerField(default=0)
    filename=models.CharField(null=True,blank=True,default="",max_length=500)
    filesize=models.IntegerField(default=0)
    down=models.IntegerField(default=0)
    
    def hitup(self):
        self.hit +=1
    def down_up(self):
        self.down +=1

class Comment(models.Model):
    idx=models.AutoField(primary_key=True)
    board_idx=models.IntegerField(null=False)
    writer=models.CharField(null=False,max_length=50)
    content=models.TextField(null=False)
    post_date=models.DateTimeField(default=datetime.now,blank=True)










    