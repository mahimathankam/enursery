from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to='media/images',blank=True,null=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    contact_name=models.CharField(max_length=100)
    email=models.EmailField()
    number=models.IntegerField()
    message=models.TextField()
    def __str__(self):
        return self.contact_name

class Product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='images/products',null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Deal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    quantity=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        if self.product:
            return self.quantity * self.product.price
        elif self.deal:
            return self.quantity * self.deal.price
        else:
            return 0

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    no_of_items=models.IntegerField()
    address=models.TextField()
    phone=models.IntegerField()
    order_status=models.CharField(max_length=20,default='pending')
    delivery_status=models.CharField(max_length=20,default='pending')
    ordered_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name

class Account(models.Model):
    accntnum=models.IntegerField()
    accnttype=models.CharField(max_length=20)
    amount=models.IntegerField()
    def __str__(self):
        return str(self.accntnum)


