from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Product,ProductUser
from .serializers import ProductSerializer,ProductUserSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from django.contrib.auth.models import User
from .producer import publish
import json

import random

class ProductViewSet(viewsets.ViewSet):
    def list(self,request): #/api/products
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    
class UserAPIView(APIView):
    def post(self,request,pk): 
        req=requests.get('http://docker.for.mac.localhost:8000/api/users')
        us=req.json()
        data={'user_id':us["id"],'product_id':int(pk)}
        try:
            product_user=ProductUserSerializer(data=data)
            if product_user.is_valid():
                product_user.save()
                publish('product_liked',pk)
                return Response(product_user.data,status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_409_CONFLICT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
