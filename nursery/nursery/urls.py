"""
URL configuration for nursery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from garden import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name='home'),
    path("category",views.category,name='category'),
    path("product/<p>",views.product,name='product'),
    path("detail/<p>",views.detail,name='detail'),
    path("register", views.register, name='register'),
    path("login", views.user_login, name='login'),
    path("logout",views.user_logout,name='logout'),
    path("addcart/<p>",views.cart,name='pcart'),
    path('addcart/deal/<p>',views.cart, {'deal': True}, name='dcart'),
    path("viewcart",views.cartview,name='view'),
    path("deletecart/<p>", views.deletecart,name='pdcart'),
    path('deletecart/deal/<p>', views.deletecart, {'deal': True}, name='ddcart'),
    path("removecart/<p>", views.removecart,name='prcart'),
    path('removecart/deal/<p>', views.removecart, {'deal': True}, name='drcart'),
    path('orderform',views.orderform,name='orderform'),
    path("orderview",views.orderview, name='orderview'),
    path('blog',views.blog,name='blog'),
    path('deal',views.deal,name='deal'),
    path('contact',views.contact,name='contact'),
    path('thank',views.thank,name='thank'),
    path('search',views.search,name='search'),



]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)