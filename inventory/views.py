from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, pk=None):
        """
        Override the retrieve method to use cache when fetching a single item.
        """
        item = get_item(pk)  # Use the caching function to retrieve the item
        if item:
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        else:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

# Caching logic
def get_item(item_id):
    # Try to get the item from the cache
    item = cache.get(f'item_{item_id}')
    
    # If it's not in the cache, retrieve from the database and cache it
    if not item:
        try:
            item = Item.objects.get(id=item_id)
            cache.set(f'item_{item_id}', item)  # Cache the item
        except Item.DoesNotExist:
            item = None
    
    return item
