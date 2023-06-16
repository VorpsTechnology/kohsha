from django.db import models
class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name