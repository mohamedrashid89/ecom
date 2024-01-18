from django.contrib import admin
from .models import *

# Register your models here.


class ImagesTabularinline(admin.TabularInline):
    model = Images

class TagTabularinline(admin.TabularInline):
    model = Tag


admin.site.register(Images)
admin.site.register(Tag)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ImagesTabularinline,TagTabularinline]
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Product, ProductAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(ContactForm)
admin.site.register(FaqForm)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Category, CategoryAdmin)
admin.site.register(Color)

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['product_status']
    list_display = ['user', 'price', 'order_date', 'product_status' ]

admin.site.register(CartOrder, CartOrderAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating' ]

admin.site.register(ProductReview, ProductReviewAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

admin.site.register(Wishlist_model, WishlistAdmin)


# class CartOrderItemsAdmin(admin.ModelAdmin):
#     list_display = ['order', 'item', 'image', 'qty', 'price']

# admin.site.register(CartOrderItems, CartOrderItemsAdmin)

class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'item_price']
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)

# class AddressAdmin(admin.ModelAdmin):
admin.site.register(Address)
admin.site.register(NewsletterSubscriber)


 
 