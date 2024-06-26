from django.shortcuts import render,redirect
from django.db.models import Q
from garden.models import Category,Product,Cart,Account,Order,Contact,Deal
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    cat = Category.objects.all()
    if request.method=='POST':
        n = request.POST['n']
        e = request.POST['e']
        num = request.POST['num']
        m = request.POST['m']
        c=Contact.objects.create(contact_name=n,email=e,number=num,message=m)
        return thank(request)

    return render(request,'home.html',{"cat":cat})

def category(request):
    c = Category.objects.all()
    return render(request,'category.html',{"cat":c})

def thank(request):
    return render(request,'thankyou.html')

def product(request,p):
    c = Category.objects.get(name=p)
    pr=Product.objects.filter(category=c)
    return render(request,'product.html',{'prod':pr})

def detail(request,p):
    b=Product.objects.get(name=p)
    return render(request,'detail.html',{'b':b})

def blog(request):
    return render(request,'blog.html')

def deal(request):
    d=Deal.objects.all()
    return render(request,'deal.html',{'deals':d})

def contact(request):
    if request.method=='POST':
        n = request.POST['n']
        e = request.POST['e']
        num = request.POST['num']
        m = request.POST['m']
        c=Contact.objects.create(contact_name=n,email=e,number=num,message=m)
        return thank(request)

    return render(request,'contact.html')

def register(request):
    if(request.method=='POST'):
        u=request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['em']
        if(p==cp):
            user = User.objects.create_user(username=u, password=p, first_name=f,last_name=l, email=e)
            user.save()
            return redirect('home')
        else:
            return HttpResponse("Passwords doesn't match")
    return render(request,'register.html')

def user_login(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if(user):
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def search(request):
    query=""
    b=None
    if(request.method=='POST'):
        query=request.POST['q']
        if(query):
            b=Product.objects.filter(Q(name__icontains=query)| Q(desc__icontains=query))

    return render(request,template_name='search.html',context={'query':query,'b':b})

@login_required
def cartview(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    total = 0
    for item in c:
        if item.product:
            total += item.quantity * item.product.price
        elif item.deal:
            if item.deal.price:
                total += item.quantity * item.deal.price

    return render(request, 'cart.html', {'c': c, 'total': total})



@login_required
def cart(request,p,deal=False):
    if deal:
        product = Deal.objects.get(title=p)
    else:
        product = Product.objects.get(name=p)

    user = request.user
    try:
        if deal:
            cart_item = Cart.objects.get(user=user, deal=product)
        else:
            cart_item = Cart.objects.get(user=user, product=product)

        if product.stock > 0:
            cart_item.quantity += 1
            cart_item.save()
            product.stock -= 1
            product.save()
    except Cart.DoesNotExist:
        if product.stock > 0:
            if deal:
                cart_item = Cart.objects.create(deal=product, user=user, quantity=1)
            else:
                cart_item = Cart.objects.create(product=product, user=user, quantity=1)
            product.stock -= 1
            product.save()

    return cartview(request)


@login_required
def deletecart(request,p,deal=False):
    if deal:
        product = Deal.objects.get(title=p)
    else:
        product = Product.objects.get(name=p)

    user = request.user
    try:
        if deal:
            cart_item = Cart.objects.get(user=user, deal=product)
        else:
            cart_item = Cart.objects.get(user=user, product=product)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            product.stock += 1
            product.save()
        else:
            cart_item.delete()
            product.stock += 1
            product.save()
    except Cart.DoesNotExist:
        pass

    return cartview(request)


@login_required
def removecart(request,p,deal=False):
    if deal:
        product = Deal.objects.get(title=p)
    else:
        product = Product.objects.get(name=p)

    user = request.user
    try:
        if deal:
            cart_item = Cart.objects.get(user=user, deal=product)
        else:
            cart_item = Cart.objects.get(user=user, product=product)

        cart_item.delete()
        product.stock += cart_item.quantity
        product.save()
    except Cart.DoesNotExist:
        pass

    return cartview(request)


@login_required
def orderform(request):
    if(request.method=='POST'):
        a=request.POST['a']
        p= request.POST['p']
        ac=request.POST['ac']

        u=request.user
        c=Cart.objects.filter(user=u)

        total = 0
        for i in c:
            if i.product is not None:
                total += i.quantity * i.product.price
            else:
                print(f"Warning: Cart item {i.id} has no associated product.")


        try:
            n=Account.objects.get(accntnum=ac)
            if(n.amount>=total):
                n.amount=n.amount-total
                n.save()

                for i in c:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status='paid')
                    o.save()
                c.delete()
                msg="Your order placed successfully"
                return render(request,'orderdetail.html',{'msg':msg})
            else:
                msg='Insufficient amount.You cant Place order'
                return render(request,'orderdetail.html',{'msg':msg})
        except:
            pass

    return render(request,'orderform.html')

@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'order':o,'u':u})