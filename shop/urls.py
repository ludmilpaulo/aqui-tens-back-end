from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopCategoryViewSet, ShopViewSet, get_shops_by_category

router = DefaultRouter()
router.register('shop-categories', ShopCategoryViewSet)
router.register('shops', ShopViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-shops-by-category/', get_shops_by_category, name='get_shops_by_category'),
]
