from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .models import ShopCategory, Shop
from .serializers import ShopCategorySerializer, ShopSerializer

class ShopCategoryViewSet(viewsets.ModelViewSet):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategorySerializer

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def list(self, request, *args, **kwargs):
        category_slug = request.query_params.get('category_slug')
        if category_slug:
            category = ShopCategory.objects.filter(slug=category_slug).first()
            if category:
                queryset = self.queryset.filter(shop_category=category)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
        return super().list(request, *args, **kwargs)



def get_shops_by_category(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
                shops = Shop.objects.filter(shop_category_id=category_id)
                # Assuming you have a serializer for Shop model
                data = [{'id': shop.id, 'name': shop.name, 'phone': shop.phone, 'address': shop.address} for shop in shops]
                return JsonResponse(data, safe=False)
            except ValueError:
                return JsonResponse({'error': 'Invalid category ID'}, status=400)
        else:
            return JsonResponse({'error': 'Category ID is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
