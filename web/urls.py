from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name='index'),
    path("cart/", views.cart_view, name='cart'),
    path("shop/", views.shop, name='shop'),
    path("checkout", views.checkout_view, name='checkout'),

    path("wishlist/", views.wishlist_view, name='wishlist'),
    

    path("shop/<slug:slug>/", views.shop_details, name='shop_detail'),
    path("blog", views.blog, name='blog'),
    path("blog/<slug:slug>/", views.blog_details, name='blog_details'),
    path("contact", views.contact, name='contact'),
    path("about", views.about, name='about'),
    path("error", views.error_404_view, name='error'),
    path("faq", views.faq, name='faq'),
    path('logout/', views.Logout, name='logout'),
    path('login/', views.login_page, name='log'),
    path("register", views.register, name='register'),

    # add review
    path("ajax-add-review/<int:id>", views.ajax_add_review, name="ajax-add-review"),

    # Search
    path("search/",views.search_view,name="search"),


    # Add to Cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    
   
    #Delete Items
    path("delete-from-cart/", views.delete_item_from_cart, name="delete-from-cart"),
    
    #Update Items
    path("update-cart/", views.update_cart, name="update-cart"),
    
    # Paypal Integration
    path('paypal/', include("paypal.standard.ipn.urls")),
    
    #Payment Successfully
    path("payment-completed/", views.payment_completed_view, name="payment-completed"),
    
    #Payment Failed
    path("payment-failed/", views.payment_failed_view, name="payment-failed"),
    
    # add to wishlist
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),
    
    # Remove Wishlist
    path("remove-from-wishlist/<int:product_id>/", views.remove_wishlist, name="remove-from-wishlist"),

    
    path("filter-product/", views.filter_product, name="filter-product"),
    
    
]
