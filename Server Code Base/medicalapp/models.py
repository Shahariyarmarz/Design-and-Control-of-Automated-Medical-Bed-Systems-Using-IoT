from django.db import models

# Create your models here.

class robo(models.Model):
    Robot=models.CharField(max_length=30,blank=False)
    Value=models.IntegerField(blank=False)
    Type = models.CharField(max_length=10, blank=True, null=True)
    OT_call = models.IntegerField(blank=False, null=True)
    Position_leave = models.IntegerField(blank=False, null=True)
    
    def __str__(self):
        return self.Robot