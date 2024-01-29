from .models import *
from django.contrib.auth.models import AnonymousUser


def default(request):
    
    wishlist_count = 0
    
    if request.user.is_authenticated:
        wishlist = WishlistItem.objects.filter(user=request.user)
        wishlist_count = wishlist.count()
      
    
    return {
        'wishlist_count': wishlist_count,
    }