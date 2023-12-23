import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

invasion = False
smoke_sensor = True


channel.queue_declare(queue='security_energy')

if invasion is True:
    security = "Invasion detected"
    channel.basic_publish(exchange='', routing_key='security_energy', body=security)
    print(" [x] Sent: ", security)
if smoke_sensor is True:
    security = "Smoke detected"
    channel.basic_publish(exchange='', routing_key='security_energy', body=security)
    print(" [x] Sent: ", security)
if invasion is False and smoke_sensor is False:
    security = "It`s OK"
    channel.basic_publish(exchange='', routing_key='security_energy', body=security)
    print(" [x] Sent: ", security)


connection.close()