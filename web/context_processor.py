from .models import *
from django.contrib.auth.models import AnonymousUser
from django.db.models import Min, Max 

def default(request):
    
    # Price Range
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    
    wishlist_count = 1
    
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist_model.objects.filter(user=request.user)
            wishlist_count = wishlist.count()
        except Wishlist_model.DoesNotExist:
            pass
    
    return {
        'wishlist_count': wishlist_count,
        'min_max_price': min_max_price, 
    }