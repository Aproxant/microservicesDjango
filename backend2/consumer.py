import pika
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend2.settings")
import django
django.setup()

from base.models import Product
from base.serializers import ProductSerializer
params=pika.URLParameters('')

connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='main')

def callback(ch,method,properties,body):
    print('Received in main')
    data=json.loads(body)
    print(data)
    if properties.content_type=='product_created':
        serializer=ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    elif properties.content_type=='product_updated':
        try:
            product=Product.objects.get(id=int(data["id"]))
        except Product.DoesNotExist:
            return
            
        serializer=ProductSerializer(instance=product,data=data)
        if serializer.is_valid():
            serializer.save()

    elif properties.content_type=='product_deleted':
        try:
            product=Product.objects.get(id=int(data))
        except Product.DoesNotExist:
            return
            
        product.delete()



channel.basic_consume(queue='main', on_message_callback=callback,auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

    