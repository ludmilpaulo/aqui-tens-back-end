from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import ShopCategory, Shop, Product
from .serializers import ShopCategorySerializer, ShopSerializer, ProductSerializer

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
                data = [{'id': shop.id, 'name': shop.name, 'phone': shop.phone, 'address': shop.address, 'logo':shop.logo} for shop in shops]
                return JsonResponse(data, safe=False)
            except ValueError:
                return JsonResponse({'error': 'Invalid category ID'}, status=400)
        else:
            return JsonResponse({'error': 'Category ID is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)
    



class GetShopsByCategoryView(generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        category_id = self.request.GET.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
                return Shop.objects.filter(shop_category_id=category_id)
            except ValueError:
                return Shop.objects.none()
        else:
            return Shop.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)



from django.http import JsonResponse
from .models import Product

from django.core.serializers import serialize
from django.http import JsonResponse

def get_products_by_shop(request):
    if request.method == 'GET':
        shop_id = request.GET.get('shop_id')
        if shop_id:
            try:
                products = Product.objects.filter(seller_id=shop_id)
                serialized_products = ProductSerializer(products, many=True).data
                return JsonResponse(serialized_products, safe=False)
            except ValueError:
                return JsonResponse({'error': 'Invalid shop ID'}, status=400)
        else:
            return JsonResponse({'error': 'Shop ID is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only GET method is allowed'}, status=405)


