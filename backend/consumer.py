import pika
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
django.setup()

from products.models import Product


params=pika.URLParameters('')

connection=pika.BlockingConnection(params)

channel=connection.channel()

channel.queue_declare(queue='main1')

def callback(ch,method,properties,body):
    print('Received in admin')
    data=json.loads(body)
    print(data)
    try:
        product=Product.objects.get(id=data)
    except:
        return 
    product.likes=product.likes+1
    product.save()

channel.basic_consume(queue='main1', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()

    