from django.contrib import admin
from django.urls import path
from .views.home import Index ,store,productView,admin_dashboard_view,delete_customer_view,view_customer_view,admin_view_booking_view,delete_order_view,update_order_view,admin_products_view,update_product_view,delete_product_view,update_customer_view,useradmin_base,store_order,manage_account,customer_address_view,payment_success_view,my_order_view,download_invoice_view

from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.contact import contact
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView
from .views.home import admin_add_product_view
from .middlewares.auth import  auth_middleware

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('contact', contact, name='contact'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('store/productpage/<int:id>/',productView, name='productView'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('view-customer', view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', update_customer_view,name='update-customer'),
    path('delete-product/<int:pk>', delete_product_view,name='delete-product'),

    #---admin Dashboard url

    path('adminlogin', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('admin-add-product',admin_add_product_view,name='admin-add-product'),
    path('admin-products', admin_products_view,name='admin-products'),
    path('update-product/<int:pk>', update_product_view,name='update-product'),
    path('admin-dashboard',admin_dashboard_view,name='admin-dashboard'),
    path('admin-view-booking', admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', delete_order_view,name='delete-order'),
    path('update-order/<int:pk>',update_order_view,name='update-order'),
    

    #--user Dashboard url
    path('customer-address', customer_address_view,name='customer-address'),
    path('useradmin_base',useradmin_base,name='useradmin_base'),
    path('storeorder',store_order,name='storeorder'),
    path('manageAccount',manage_account,name='manageAccount'),
    # path('trackOrder',update_order,name='trackOrder'),
    path('my-order',my_order_view,name='my-order'),
    path('payment-success',payment_success_view,name='payment-success'),
    path('download-invoice/<int:orderID>/<int:productID>',download_invoice_view,name='download-invoice'),   

]
