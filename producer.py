import pika
from faker import Faker
import connect
from models import Contact

fake = Faker()

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='email_queue')

for _ in range(10):
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number()
    )
    contact.save()

    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=str(contact.id)
    )

print("Contacts created and sent to queue.")
connection.close()