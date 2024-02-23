from django.contrib import admin
from django.urls import path
from .views import ProductViewSet,UserAPIView
urlpatterns = [
    path('products', ProductViewSet.as_view({
        'get':'list',
    })),
        
    path('products/<int:pk>/like', UserAPIView.as_view())
]