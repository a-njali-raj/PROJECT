
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name="home"),
    path('index.html',views.index,name="home"),
    path('about.html',views.about,name="about"),
    path('services.html',views.services,name="services"),
    path('contact.html',views.contact,name="contact"),
    path('login.html',views.loginn,name="login"),
    path('signup.html',views.signup,name="signup"),
    path('appoinment.html',views.appoinment,name="appoinment"),
    path('payment/<str:order_id>/',views.payment,name="payment"),
    path('user.html',views.user,name="user"),
    path('logout/',views.logout,name="logout"),
    path('services1.html',views.services1,name="services1"),
    path('check_username_availability/', views.check_username_availability, name='check_username_availability'),
    path('check_email_availability/', views.check_email_availability, name='check_email_availability'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('userprofile.html',views.userprofile,name="userprofile"),
    path('updateprofile.html',views.updateprofile,name="updateprofile"),
    path('get_test_price/', views.get_test_price, name='get_test_price'),
    path('verify-payment/',views.verify_payment, name="verify-payment"),
    path('review/',views.Review_rate,name="review"),
    path('myappoinment',views.myappoinment,name="myappoinment") ,
    path('payment_success',views.payment_success,name="payment_success") ,
    path('product.html',views.product_list,name="product"),
    path('product/<int:product_id>/',views.product_detail,name="product_detail"),
    path('add-to-cart/', views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('order/', views.order, name="order"),
    path('cart.html', views.cart, name='cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('product/search/', views.product_search, name='product_search'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('myorder/',views.myorder,name="myorder"),
    # path('chatgpt/', views.chatgpt, name='chatgpt'),
    # path('generate-response/', views.generate_response, name='generate_response'),
]
