from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


# Create your models here.
STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),  
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
	    return self.name

class Color(models.Model):
    color = ColorField(default='#FF0000')
    status = models.CharField(max_length=10)

    def __str__(self):
	    return self.status
    

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='Product/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # a Product can have multiple images

class Tag(models.Model):
    tag_name = models.CharField(max_length=80)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.tag_name

class BlogPost(models.Model):
    image = models.ImageField(upload_to='Post/')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    quote = models.CharField(max_length=200)
    Person_name = models.CharField(max_length=20)
    
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
class FaqForm(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
    

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(max_length=99999999999, default="1.99")
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")


class CartOrderProducts(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    item_price = models.FloatField(max_length=99999999999, default="1.99")
    total = models.FloatField(max_length=99999999999, default="1.99")
    
    
# class CartOrderItems(models.Model):
#     order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
#     item = models.CharField(max_length=200)
#     image = models.CharField(max_length=200)
#     qty = models.IntegerField(default=0)
#     price = models.FloatField(max_length=99999999999, default="1.99")


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    
    def get_rating(self):
        return self.rating
    

class Wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    
    
class Address(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    apartment_suite_unit = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255)
    state_county = models.CharField(max_length=255)
    postcode_zip = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email