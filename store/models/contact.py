from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=100,default='', blank=False, null= False)
    phone=models.CharField(default=True,max_length=10,validators=[RegexValidator('^[9,7,8,6]\d{9}$','invalid mobile number')])
    message=models.TextField()
    def __str__(self) -> str:
        return 'Message from' + self.name + ' ' + self.email