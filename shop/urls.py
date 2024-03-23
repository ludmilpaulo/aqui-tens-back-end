from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopCategoryViewSet, ShopViewSet, get_products_by_shop, get_shops_by_category, GetShopsByCategoryView

router = DefaultRouter()
router.register('shop-categories', ShopCategoryViewSet)
router.register('shops', ShopViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('get-products-by-shops/', get_products_by_shop, name='get-products-by-shops'),
    path('get-shops-by-category/', GetShopsByCategoryView.as_view(), name='get_shops_by_category'),
]
