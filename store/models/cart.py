from django.db import models
from django.contrib.auth.models import User
from store.models.customer import Customer
from .product import Products

class Cart(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product_qty=models.IntegerField(null=True,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_qty} of {self.product.name}"


    


   
    

   

  
    