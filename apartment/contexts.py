"""Context for the shopping bag."""
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Album


def bag_contents(request):
    """Return the contents of the shopping bag."""
    bag_items = []
    total = 0
    product_count = 0
    product_item_total = 0
    bag = request.session.get('bag', {})
    if bag:
        for slug, item_data in bag.items():
            if isinstance(item_data, int):
                product_count += item_data
                product_inventory = get_object_or_404(
                    Album, slug=slug
                )
                product_item_total = product_inventory.real_price * item_data
                total += product_inventory.real_price * item_data
                bag_items.append({
                    'product_inventory': product_inventory,
                    'product_item_total': product_item_total,
                    'quantity': item_data,
                })
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'product_item_total': product_item_total,
    }
    return context
