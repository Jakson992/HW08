import json
from time import sleep
import pika
from mongoengine import *

connect(db="web12", host="mongodb+srv://JekaWEB12:567234@cluster0.plizfca.mongodb.net/?retryWrites=true&w=majority")

class Contact(Document):
    fullname = StringField(max_length=120, required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)
    # Додайте інші поля за необхідністю

def send_email(contact):
    # Логіка надсилання повідомлення по електронній пошті
    # Ви можете замінити цей код на реальну реалізацію надсилання пошти

    # Після надсилання повідомлення оновлюємо логічне поле `message_sent` для контакту
    contact.message_sent = True
    contact.save()

def process_message(channel, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    # Отримуємо контакт з бази даних за його ObjectID
    contact = Contact.objects(id=contact_id).first()

    if contact:
        send_email(contact)
        print(f"Email sent to {contact.fullname}")

    # Підтвердження обробки повідомлення
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Налаштування підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Оголошення черги
    channel.queue_declare(queue='contact_queue', durable=True)

    # Вказуємо, що кожен споживач отримує лише одне повідомлення одночасно
    channel.basic_qos(prefetch_count=1)

    # Встановлюємо зв'язок між чергою та функцією обробки повідомлень
    channel.basic_consume(queue='contact_queue', on_message_callback=process_message)

    print("Waiting for messages. To exit press CTRL+C")

    # Запуск споживача повідомлень
    channel.start_consuming()

if __name__ == "__main__":
    main()
