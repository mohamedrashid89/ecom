from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from .models import *
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProductReviewForm, CheckoutForm
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Min, Max 
from django.template.loader import render_to_string
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.core import serializers
# from django.views.generic import View

# Create your views here.

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            NewsletterSubscriber.objects.create(email=email)
            messages.success(request, 'Thank you for subscribing!')
            
            
    products = Product.objects.filter(available=True)
    images = Images.objects.all()
    
    context = {
        "products": products,
        "images": images,
    }

    return render(request, 'web/index.html', context)


def shop(request):
    categories = Category.objects.all()
    categoryId = request.GET.get('categories')
    tagId = request.GET.get('tags')

    # Start with all products
    products = Product.objects.filter(available=True)

    # Filter by category if categoryId is provided
    if categoryId:
        category = get_object_or_404(Category, slug=categoryId)
        products = products.filter(category=category)

    # Filter by tag if tagId is provided
    if tagId:
        tag = get_object_or_404(Tag, slug=tagId)
        products = products.filter(tag=tag)

    # Get min and max price based on filtered products
    min_price = products.aggregate(Min('price'))
    max_price = products.aggregate(Max('price'))

    FilterPrice = request.GET.get('FilterPrice')

    if FilterPrice is not None:
        try:
            Int_FilterPrice = int(FilterPrice)
            # Filter products based on the selected price
            products = products.filter(price__lte=Int_FilterPrice)
        except ValueError:
            # Handle the case where the conversion to integer fails
            # You might want to log the error or handle it in a way that makes sense for your application
            pass
    
    # Context setup
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        'min_price': min_price['price__min'],
        'max_price': max_price['price__max'],
        'FilterPrice': FilterPrice,
    }
    
    return render(request, 'web/shop-sidebar.html', context)



def category_links(request, slug):
    categories = Category.objects.all(slug=slug)
    return {'categories':categories}



def shop_details(request, slug):
    

    product = get_object_or_404(Product, slug=slug)

    # Getting all review
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting Average Review
    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_reviews_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_reviews_count > 0:
             make_review = False

    tags = Tag.objects.all()
    images = Images.objects.all()
    
    products = Product.objects.all()

    context = {
        'p': product,
        'tags': tags,
        'images': images,
        'reviews': reviews,
        'avg_rating' : avg_rating,
        'review_form': review_form,
        'make_review': make_review,
        'products': products
        
    }

    return render(request, 'web/shop-details.html', context)


def blog(request):
    categories = Category.objects.all()

    categoryId = request.GET.get('categories')
    if categoryId:
        category = get_object_or_404(Category, slug=categoryId)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)

    posts = BlogPost.objects.all()

    context = {
        "posts": posts,
        "categories": categories,
        'products': products,
        
    }
    return render(request, 'web/blog.html', context)



def blog_details(request, slug):
    categories = Category.objects.all()

    categoryId = request.GET.get('categories')
    if categoryId:
        category = get_object_or_404(Category, slug=categoryId)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)
   
    posts = BlogPost.objects.get(slug=slug)

    context = {
        "post": posts,
        "categories": categories,
        'products': products,
        
    }
    return render(request, 'web/blog-details.html', context)



def contact(request):
   
    if request.method == 'POST':
        contact = ContactForm()

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.message = message
        
        contact.save()
        return JsonResponse({'success': True})
    else:
        return render(request, 'web/contact.html')



def about(request):
    

    context = {
       
    }
    return render(request, 'web/about.html', context)



def error_404_view(request, exception):

    return render(request, 'web/error-404.html', {'exception': exception}, status=404)



def faq(request):
    

    if request.method == 'POST':
        faq = FaqForm()

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        faq.name = name
        faq.email = email
        faq.phone = phone
        faq.subject = subject
        faq.message = message
        
        faq.save()

        return JsonResponse({'success': True})
    else:
        return render(request, 'web/faq.html')
    

def login_page(request):
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        user = authenticate(username=username_or_email, password=password)
       

        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, "Login successful.")
            # Redirect to a home page
            return redirect('index') 
        else:
            # Login failed
            messages.error(request, "Invalid login credentials. Please try again.")

    context = {
      
    }

    return render(request, 'web/login.html', context)



def Logout(request):
    logout(request)
    return redirect('log')



def register(request):
    

    form = RegistrationForm()

    context = {
        "form": form,
    }

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('log')  # Redirect to login page or any other page you want after successful registration
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return render(request, 'web/register.html', context)



def ajax_add_review(request, id):
    product = Product.objects.get(pk=id)

    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
    }

    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
            'bool' : True,
            'context' : context,
            'avg_rating' : avg_rating,
        }

    )



def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(name__icontains=query)


    context = {
        "products": products,
        "query": query,
    }

    return render(request, 'web/search.html', context)



def add_to_cart(request):
    cart_product = {}
    
    cart_product[str(request.GET['id'])] = {
        'name': request.GET['name'],
        'price': float(request.GET['price']),
        'quantity': int(request.GET['quantity']),
        'image': request.GET['image'],
        
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = int(cart_product[str(request.GET['id'])]['quantity'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
        
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})

def cart_view(request):
        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['quantity']) * float(item['price'])
                
            return render(request, 'web/cart.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
        else:
            messages.warning(request, "Your cart is empty")
            return redirect("index")
    
    

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']            
            del request.session['cart_data_obj'][product_id]
            request.session.save()
            request.session['cart_data_obj'] = cart_data

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['quantity']) * float(item['price'])
                

    context = render_to_string("web/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])}) 



def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = int(request.GET['quantity'])
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['quantity'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
            

    context = render_to_string("web/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])}) 

 
@login_required
def checkout_view(request): 
    
    cart_total_amount = 0
    total_amount = 0
    
    # Checking if cart_data_obj session exits
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['quantity']) * float(item['price'])
    
    
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount,
        )
    
    
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
            
            cart_order_products = CartOrderProducts.objects.create(
                order=order,
                invoice_no="INVOICE_NO-" + str(order.id),
                item=item['name'],
                image=item['image'],
                quantity=int(item['quantity']),
                item_price = float(item['price']),
                total=float(item['quantity']) * float(item['price']), 
                
            )
    
    
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": cart_total_amount,
        "item_name": "Order-Item-No-"  + str(order.id),
        "invoice": "INVOICE_NO-" + str(order.id),
        "currency_code": "USD",
        "notify_url": "https://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "https://{}{}".format(host, reverse('payment-completed')),
        "cancel_return": "https://{}{}".format(host, reverse('payment-failed')),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    cart_total_amount = 0
    # Checking if cart_data_obj session exits
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price']) 
            
            
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            country = form.cleaned_data.get('country')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            company_name = form.cleaned_data.get('company_name')
            address = form.cleaned_data.get('address')
            apartment = form.cleaned_data.get('apartment')
            town_city = form.cleaned_data.get('town_city')
            state = form.cleaned_data.get('state')
            zipcode = form.cleaned_data.get('zipcode')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            
            address = Address (
                user = request.user,
                country=country,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                address=address,
                apartment_suite_unit=apartment,
                town_city=town_city,
                state_county=state,
                postcode_zip=zipcode,
                email=email,
                phone=phone,
            )
            address.save()
            order.address = address  # Associate the address with the order
            order.save()
            return redirect('checkout')
                    
    context = {
        "form": form,
        "cart_data": request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'paypal_payment_button':paypal_payment_button,
        'order':order,
    }
    

    return render(request, 'web/checkout.html', context)




@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])
            
    
    return render(request, 'web/payment-completed.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})



@login_required 
def payment_failed_view(request):
    return render(request, 'web/payment-failed.html')



@login_required 
def wishlist_view(request):

    wishlist = WishlistItem.objects.all()


        
    context = {
        'wishlist_items': wishlist,
    }
    
    return render(request, 'web/wishlist.html', context)



@login_required 
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print("Product id is:" + product_id)
    
    context = {}
    
    wishlist = WishlistItem.objects.filter(product=product, user=request.user).count()
    print(wishlist)
    
    # Calculate updated wishlist_count
    wishlist_count = WishlistItem.objects.filter(user=request.user).count()
    
    
    if wishlist > 0:
        context = {
            "bool": True,
            
        }
    else:
        new_wishlist = WishlistItem.objects.create(
            product=product,
            user=request.user
        )
        wishlist_count += 1 
        context = {
                "bool": True,
                'wishlist_count': wishlist_count,
        }
            
    return JsonResponse(context)


def remove_wishlist(request, product_id):
    wishlist_item = get_object_or_404(WishlistItem, id=product_id, user=request.user)
    wishlist_item.delete()

    wishlist_count = WishlistItem.objects.filter(user=request.user).count()

    response_data = {
        'wishlist_count': wishlist_count
    }

    return JsonResponse(response_data)


def filter_product(request):
    
    products = Product.objects.all()


    # Render the filtered product data
    data = render_to_string("web/shop-sidebar.html", {'products': products})
    
    return JsonResponse({"data": data})

