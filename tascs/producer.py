import json
import random
import string
from faker import Faker
from mongoengine import *
import pika

connect(db="web12", host="mongodb+srv://JekaWEB12:567234@cluster0.plizfca.mongodb.net/?retryWrites=true&w=majority")

fake = Faker()

class Contact(Document):
    fullname = StringField(max_length=120, required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)
    # Додайте інші поля за необхідністю

def create_fake_contact():
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()
    return contact

def publish_message(channel, message):
    channel.basic_publish(
        exchange='',
        routing_key='contact_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Зробити повідомлення стійким
    )

def main():
    # Налаштування підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Оголошення черги
    channel.queue_declare(queue='contact_queue', durable=True)

    # Генерація фейкових контактів та публікація повідомлення в чергу
    for _ in range(10):
        contact = create_fake_contact()
        message = {'contact_id': str(contact.id)}
        publish_message(channel, message)

    # Закриття з'єднання з RabbitMQ
    connection.close()

if __name__ == "__main__":
    main()
