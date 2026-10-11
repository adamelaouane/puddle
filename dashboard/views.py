from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from item.models import Item


@login_required
def index(request):
    # Get only the products created by the logged-in user
    items = Item.objects.filter(
        created_by=request.user
    ).order_by('-created_at')

    # Search products by name or description
    query = request.GET.get('query', '')

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # Statistics for all the user's products
    user_items = Item.objects.filter(created_by=request.user)

    total_products = user_items.count()
    sold_products = user_items.filter(is_sold=True).count()
    available_products = user_items.filter(is_sold=False).count()

    context = {
        'items': items,
        'query': query,
        'total_products': total_products,
        'sold_products': sold_products,
        'available_products': available_products,
    }

    return render(request, 'dashboard/index.html', context)