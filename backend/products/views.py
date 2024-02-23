from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status

from .producer import publish

from django.contrib.auth.models import User



import random

class ProductViewSet(viewsets.ViewSet):
    def list(self,request): #/api/products
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

    def create(self,request): #/api/products
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_created',serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None): #/api/products<str:pk>
        try:
            products=Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer=ProductSerializer(products)
        return Response(serializer.data)

    def update(self,request,pk=None): #/api/products<str:pk>
        try:
            products=Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=ProductSerializer(instance=products,data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('product_updated',serializer.data)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None): #/api/products<str:pk>
        try:
            products=Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        products.delete()
        publish('product_deleted',pk)

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserAPIView(APIView):
    def get(self,_):
        users=User.objects.all()
        user=random.choice(users)
        return Response({
            'id': user.id
        })
