from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from .models import *
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProductReviewForm
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Min, Max 
from django.template.loader import render_to_string
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.core import serializers

# Create your views here.

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            NewsletterSubscriber.objects.create(email=email)
            
            
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

    if categoryId:
        category = get_object_or_404(Category, slug=categoryId)
        products = Product.objects.filter(category=category, available=True)
    else:
        products = Product.objects.filter(available=True)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    context = {
        'products': products,
        'categories': categories,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # This request was made with AJAX
        return render(request, 'web/product_list.html', context)  # Update with the appropriate template
    else:
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


# @login_required
@login_required(login_url='log')
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
   
    form = ContactForm(request.POST or None)
    context = {
        "is_contact": True,
        "form": form,
    }

    if request.method == "POST":
        if form.is_valid():
            form.save()

        else:
            print(form.errors)
        

    return render(request, 'web/contact.html', context)


def about(request):
    

    context = {
       
    }
    return render(request, 'web/about.html', context)


def error(request):
    

    context = {
       
    }
    return render(request, 'web/error-404.html', context)


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

    context = {
        
      
    }


    return render(request, 'web/faq.html', context)


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
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
             cart_data = request.session['cart_data_obj']
             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty']) 
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
            if 'price' in item and item['price']:
                # Define 'item_price' before using it
                item_price = float(item['price'].replace('$', ''))
                cart_total_amount += int(item['qty']) * item_price
                
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
            request.session['cart_data_obj'] = cart_data

        cart_total_amount = 0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                if 'price' in item and item['price']:
                # Define 'item_price' before using it
                    item_price = float(item['price'].replace('$', ''))
                    cart_total_amount += int(item['qty']) * item_price

    context = render_to_string("web/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])}) 


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            if 'price' in item and item['price']:
                item_price = float(item['price'])
                cart_total_amount += int(item['qty']) * item_price

    context = render_to_string("web/cart-list.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])}) 

@login_required
def checkout_view(request):
    
    if request.method == "POST":
        user = User.objects.get(id=id)
        
        country = request.POST.get("country")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        companyname = request.POST.get("companyname")
        address = request.POST.get("address")
        apartment = request.POST.get("apartment")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postcode = request.POST.get("postcode")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        
        
        order = CartOrder (
            user = user,
            country = country,
            first_name = firstname,
            last_name = lastname,
            company_name = companyname,
            address = address,
            apartment_suite_unit = apartment,
            town_city = city,
            state_county = state,
            postcode_zip = postcode,
            email = email,
            phone = phone
        )
        order.save()
    
    
    cart_total_amount = 0
    total_amount = 0
    
    # Checking if cart_data_obj session exits
    if 'cart_data_obj' in request.session:
        # Getting total amount for Paypal Amount
        for p_id, item in request.session['cart_data_obj'].items():
            if 'price' in item and item['price']:
                # Define 'item_price' before using it
                item_price = float(item['price'].replace('$', ''))
                cart_total_amount += int(item['qty']) * item_price
                
                
        # Create Order Object
        order = CartOrder.objects.create(
            user=request.user,
            price=total_amount
        )
    

        # Getting total amount for the cart

  
        for p_id, item in request.session['cart_data_obj'].items():
            if 'price' in item and item['price']:
                # Define 'item_price' before using it
                item_price = float(item['price'].replace('$', ''))
                cart_total_amount += int(item['qty']) * item_price
    
            cart_order_products = CartOrderProducts.objects.create(
                order=order,
                invoice_no="INVOICE_NO" + str(order.id),
                item=item['name'],
                image=item['image'],
                qty=item['qty'],
                item_price=float(item['price'].replace('$', '')),
                total=int(item['qty']) * item_price,
            )
    
    
    
    


    return render(request, 'web/checkout.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})

@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            item_price = float(item['price'].replace('$', ''))
            cart_total_amount += int(item['qty']) * item_price
            
            
            
    return render(request, 'web/payment-completed.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})

@login_required 
def payment_failed_view(request):
    return render(request, 'web/payment-failed.html')

@login_required 
def wishlist_view(request):

    wishlist = Wishlist_model.objects.all()

        
    context = {
        'w': wishlist,
    }
    
    return render(request, 'web/wishlist.html', context)

@login_required 
def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print("Product id is:" + product_id)
    
    context = {}
    
    wishlist = Wishlist_model.objects.filter(product=product, user=request.user).count()
    print(wishlist)
    
    # Calculate updated wishlist_count
    wishlist_count = Wishlist_model.objects.filter(user=request.user).count()
    
    
    if wishlist > 0:
        context = {
            "bool": True,
            
        }
    else:
        new_wishlist = Wishlist_model.objects.create(
            product=product,
            user=request.user
        )
        context = {
                "bool": True,
                'wishlist_count': wishlist_count,
        }
            
    return JsonResponse(context)

    
    
def remove_wishlist(request):
    try:
        id = request.GET['id']
        wishlist = Wishlist_model.objects.filter(user=request.user)

        wishlist_d = get_object_or_404(Wishlist_model, id=id, user=request.user)
        
        wishlist_d.delete()
        
        wishlist_count = wishlist.count()


        context = {
            "bool": True,
            "w": wishlist
        }

        wishlist_json = serializers.serialize('json', wishlist)

        data = render_to_string("web/wishlist-list.html", context)

        return JsonResponse({"data": data, "w": wishlist_json, "wishlist_count": wishlist_count})
    except Wishlist_model.DoesNotExist:
        # Handle the case where the wishlist with the given id does not exist
        return JsonResponse({"error": "Wishlist not found"}, status=404)