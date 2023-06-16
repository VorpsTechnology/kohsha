from django.db import models
from .product import Products
from .customer import Customer
from django.utils import timezone
from django.shortcuts import reverse
from .cart import Cart
import datetime


# Order
ORDER_STATUS = (
    ('Preparing', 'Preparing'),
    ('Shipping', 'Shipping'),
    # ('Picked up from store', 'Picked up from store'),
    # ('Out for delivery', 'Out for delivery'),
    ('Delivered', 'Delivered'),
    ('RETURNED', 'RETURNED'),
    ('CANCELED', 'CANCELED')
)

# Return
RETURN_STATUS = (
    ('Processing Return Request', 'Processing Return Request'),
    ('Item Received by Vendor', 'Item Received by Vendor'),
    ('Return Denied', 'Return Denied'),
    ('Return Granted', 'Return Granted'),
)


RETURN_REASON = (
    ('Damaged', 'Damaged'),
    ('Expired', 'Expired'),
    ('Ordered Wrong Item', 'Ordered Wrong Item'),
    ('Received Wrong Item', 'Received Wrong Item'),
    ('Received Wrong Brand Item', 'Received Wrong Brand Item'),  # may be variation
    ('Other', 'Other')
)


# Cancel
CANCEL_REASON = (
    ('Not Needed', 'Not Needed'),
    ('Ordered Wrong Product', 'Ordered Wrong Product'),
    ('Receiving To Late', 'Receiving To Late'),
    ('Select Different Payment Method', 'Select Different Payment Method'),
    ('Other', 'Other')
)

CANCEL_STATUS = (
    ('Processing Cancel Request', 'Processing Cancel Request'),
    ('CANCEL Denied', 'CANCEL Denied'),
    ('Cancel Granted', 'Cancel Granted'),
)

class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    date = models.DateField (default=datetime.datetime.today)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    weight = models.IntegerField(default=False)
    city = models.CharField(max_length=50,default='Delhi')
    state = models.CharField(max_length=50,default='Delhi')
    zipcode = models.CharField(max_length=10,null=True)
    order_id = models.CharField(max_length=200, null=True, blank=True)
    order_ref_number = models.CharField(unique=True, default='ORD-100000', max_length=15)
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
    'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    received = models.BooleanField(default=False, blank=True, null=True)
    payment_method = models.CharField(default='Online by card', max_length=30)
    taxes = models.FloatField(default=0)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
class ReturnMiniOrder(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    return_requested = models.BooleanField(default=True)
    return_status = models.CharField(choices=RETURN_STATUS, max_length=50, default='Processing Return Request')
    return_granted = models.BooleanField(default=False)

    return_date = models.DateTimeField(default=timezone.now)
    return_reason = models.CharField(choices=RETURN_REASON, max_length=50, blank=True, null=True)
    review_description = models.TextField(help_text='Please Describe in detail reason of return.')

    return_order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ['return_date']

    def __str__(self):
        return f"{self.user}_{self.return_reason}_RETURNED"

    def get_absolute_url(self):  # Redirect to this link after filling the form for return order
        return reverse("order-all")
    
class CancelOrder(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    cancel_requested = models.BooleanField(default=True)
    cancel_status = models.CharField(choices=CANCEL_STATUS, max_length=50, default='Processing Cancel Request')
    cancel_granted = models.BooleanField(default=False)

    cancel_date = models.DateTimeField(default=timezone.now)
    cancel_reason = models.CharField(choices=CANCEL_REASON, max_length=50, blank=True, null=True)
    review_description = models.TextField(help_text='Please Describe in detail reason of cancel.')
    cancel_order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user}_{self.cancel_reason}_CANCELED"

    def get_absolute_url(self):  # Redirect to this link after filling the form for cancel order
        return reverse("order-all")

    class Meta:
        ordering = ['-cancel_date']


class Payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=200)
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    amount_paid = models.FloatField()
    currency = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}_Payment"
    

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

def __str__(self):
    return self.update_desc[0:7] + "..."

