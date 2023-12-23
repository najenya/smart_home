import pika

def send_request(channel, request_queue, request):
    channel.basic_publish(exchange='', routing_key=request_queue, body=request)
    print(" [x] Sent Request:", request)

def receive_response(ch, method, properties, body):
    decoded_message = body.decode('utf-8')
    print(f" [x] Received Response: {decoded_message}")

def make_decision(channel, request_queue, response_queue, current_temperature, optimal_temperature):
    if current_temperature > optimal_temperature:
        while current_temperature > optimal_temperature:
            send_request(channel, request_queue, f"{'Cool down'}")
            current_temperature -= 1
    if current_temperature < optimal_temperature:
        while current_temperature < optimal_temperature:
            send_request(channel, request_queue, f"{'Heat up'}")
            current_temperature += 1
    if current_temperature == optimal_temperature:
        send_request(channel, request_queue, f"{'Optimal temperature'}")

    channel.basic_consume(queue=response_queue, on_message_callback=receive_response, auto_ack=True)
    print(' [*] Waiting for response')
    channel.start_consuming()

def close_connection(connection):
    connection.close()




if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    request_queue = 'climate_energy_request'
    response_queue = 'climate_energy_response'
    channel.queue_declare(queue=request_queue)
    channel.queue_declare(queue=response_queue)

    current_temperature = 25
    optimal_temperature = 22

    try:
        make_decision(channel, request_queue, response_queue, current_temperature, optimal_temperature)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        close_connection(connection)
