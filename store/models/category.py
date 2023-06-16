from django.db import models

class Category(models.Model):
    name= models.CharField(max_length=50)
    description= models.CharField(max_length=250, default='', blank=False, null= False)
    image= models.ImageField(upload_to='uploads/category/',default='DEFAULT VALUE', blank=True, null=True)
    

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
