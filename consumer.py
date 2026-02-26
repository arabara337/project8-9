import pika
import connect
from models import Contact

def send_email_stub(contact):
    print(f"Sending email to {contact.email}")

def callback(ch, method, properties, body):
    contact = Contact.objects(id=body.decode()).first()
    if contact:
        send_email_stub(contact)
        contact.message_sent = True
        contact.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='email_queue')

channel.basic_consume(
    queue='email_queue',
    on_message_callback=callback
)

print("Waiting for messages...")
channel.start_consuming()