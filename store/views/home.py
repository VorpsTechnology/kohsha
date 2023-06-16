from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.customer import Customer
from store.models.product import Products
from store.models.contact import Contact
from store.models.category import Category
from django.views import View
from django.contrib import messages
from store.models import Cart
from store.models import Products
from django.contrib.auth.decorators import login_required,user_passes_test
from store.models import orders
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from store.forms import *


class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        quantity = request.POST.get('quantity',1)
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        customer_id = request.session.get('customer')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                        messages.success(request, "removed successfully!")
                else:
                    cart[product]  = quantity+1
                    messages.success(request, "added successfully!")
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            product = Products.objects.get(id=product)
            cart_item, created = Cart.objects.get_or_create(user=customer, product=product,product_qty=quantity)
            cart_item.save()
        print('cart' , request.session['cart'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    def get(self , request):
        # print()
        category=Category.objects.all()
        # print(category)
        context={
            'category':category,
        }
        return render(request,'home.html',context)
        # return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')



def store(request):
    cart = request.session.get('cart')
    
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    print(categories)
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
        # print(Products);
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    # for product in products:
    #     print('Product ID:', product.id)  
    return render(request, 'index.html', data)

def productView(request,id):
    product=Products.objects.filter(id=id)
    CategoryName=product[0].category
    related_product = Products.objects.filter(category=CategoryName)
    print(related_product)
    # AllCategories=product[0].category
    
    # category=Products.get_all_products_by_categoryid(AllCategories)
    # print(category);
    
    print(product[0].category)
    return render(request,'productpage.html',{'product':product[0],'related_products':related_product[0:]})
    
    # return render(request,'productpage.html',{id:'id'})

def contact(request):
     
     if request.method=='POST':
         name=request.POST.get('name')
         email=request.POST.get('email')
         phone=request.POST.get('phone')
         message=request.POST.get('message')
         contact=Contact(name=name,email=email,phone=phone,message=message)
         print(name)
         print(contact)
         contact.save()
     return render(request,'home.html')


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=Customer.objects.all()
    return render(request,'view-customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=Customer.objects.get(id=pk)
    # user=Customer.objects.get(id=customer)
    # user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=Customer.objects.get(id=pk)
    # user=Customer.objects.get(id=customer.isExists)
    # userForm=CustomerUserForm(instance=user)
    customerForm=CustomerForm(request.FILES,instance=customer)
    mydict={'customerForm':customerForm}
    if request.method=='POST':
        # userForm=CustomerUserForm(request.POST,instance=user)
        customerForm=CustomerForm(request.POST,instance=customer)
        if  customerForm.is_valid():
            # user=userForm.save()
            # user.set_password(user.password)
            # user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'admin_update_customer.html',context=mydict)


@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=Products.objects.all()
    return render(request,'admin_products.html',{'products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=ProductForm()
    if request.method=='POST':
        productForm=ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=Products.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')

@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=Products.objects.get(id=pk)
    productForm=ProductForm(instance=product)
    if request.method=='POST':
        productForm=ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'admin_update_product.html',{'productForm':productForm})

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=Customer.objects.all().count()
    productcount=Products.objects.all().count()
    ordercount=Order.objects.all().count()

    # for recent order tables
    orders=Order.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=Products.objects.all().filter(id=order.product.id)
        ordered_by=Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'admin_dashboard.html',context=mydict)


# admin add product by clicking on floating button

@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=ProductForm()
    if request.method=='POST':
        productForm=ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=Products.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=Products.objects.get(id=pk)
    productForm=ProductForm(instance=product)
    if request.method=='POST':
        productForm=ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'admin_update_product.html',{'productForm':productForm})

#--view order
@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=Order.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=Products.objects.all().filter(id=order.product.id)
        ordered_by=Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


#--delete order
@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=Order.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')


#--update order
@login_required(login_url='adminlogin')
def update_order_view(request, pk):
    order = Order.objects.get(id=pk)
    orderForm = OrderForm(instance=order)
    if request.method == 'POST':
        orderForm = OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request, 'update_order.html', {'orderForm': orderForm})


def customer_address_view(request):
    product_in_cart = False
    if 'ids' in request.session:
        ids = request.session['ids']
        if ids != "":
            product_in_cart = True

    if 'ids' in request.session:
        ids = request.session['ids']
        counter = ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    addressForm = AddressForm()
    if request.method == 'POST':
        addressForm = AddressForm(request.POST)
        if addressForm.is_valid():
            email = addressForm.cleaned_data['Email']
            phone = addressForm.cleaned_data['PHONE']
            address = addressForm.cleaned_data['Address']

            total = 0
            if 'ids' in request.session:
                ids = request.session['ids']
                if ids != "":
                    product_id_in_cart = ids.split('|')
                    products = Products.objects.filter(id__in=product_id_in_cart)
                    for p in products:
                        total += p.price

            response = render(request, 'payment.html', {'total': total})
            response.session['email'] = email
            response.session['phone'] = phone
            response.session['address'] = address
            return response

    return render(request, 'customer_address.html', {'addressForm': addressForm, 'product_in_cart': product_in_cart, 'product_count_in_cart': product_count_in_cart})






@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place an order after successful payment
    # We will fetch customer phone, address, email
    # We will fetch product IDs from the session and retrieve respective details from the database
    # Then we will create order objects and store them in the database
    # After that, we will clear the session data related to the order

    customer = Customer.objects.get(user=request.user)
    products = None
    email = None
    phone = None
    address = None

    if 'ids' in request.session:
        ids = request.session['ids']
        if ids != "":
            product_id_in_cart = ids.split('|')
            products = Products.objects.filter(id__in=product_id_in_cart)

    # Retrieve email, phone, and address from the session
    email = request.session.get('email')
    phone = request.session.get('phone')
    address = request.session.get('address')

    # Place an order for each product
    for product in products:
        Order.objects.get_or_create(
            customer=customer,
            product=product,
            status='Pending',
            email=email,
            phone=phone,
            address=address
        )

    # Clear the session data related to the order
    del request.session['ids']
    del request.session['email']
    del request.session['phone']
    del request.session['address']

    return render(request, 'payment_success.html')


#-----------for checking user iscustomer
def is_customer(Customer):
    return Customer.groups.filter(name='CUSTOMER').exists()

# @login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):
    customer = Customer.objects.get(user_id=request.id)
    orders = Order.get_orders_by_customer(customer)
    ordered_products = []

    for order in orders:
        ordered_product = order.product
        ordered_products.append(ordered_product)

    return render(request, 'my_order.html', {'data': zip(ordered_products, orders)})




def useradmin_base(request):
    return render(request,'useradmin_base.html')

def store_order(request):
    return render(request,'storeorder.html')

def manage_account(request):
    return render(request,'manageAccount.html')

#---pdf dowl
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

# @login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=Order.objects.get(id=orderID)
    product=Products.objects.get(id=productID)
    mydict={
        'orderDate':order.date,
        'customerName':request.first_name,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.image,
        'productPrice':product.price,
        'productDescription':product.description,


    }
    return render_to_pdf('download_invoice.html',mydict)








 










   

