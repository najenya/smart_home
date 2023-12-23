import pika

def send_request(channel, request_queue, request):
    channel.basic_publish(exchange='', routing_key=request_queue, body=request)
    print(" [x] Sent Request:", request)

def receive_response(ch, method, properties, body):
    decoded_message = body.decode('utf-8')
    print(f" [x] Received Response: {decoded_message}")

def make_decision(channel, request_queue, response_queue, nighttime_start, nighttime_finish, current_time):
    if current_time >= nighttime_start and current_time <= nighttime_finish:
        while current_time < nighttime_finish:
            schedule = "Night mode on"
            send_request(channel, request_queue, f"{schedule}")
            current_time += 1
        if current_time == nighttime_finish:
            schedule = "Night mode off"
            send_request(channel, request_queue, f"{schedule}")

    if current_time < nighttime_start or current_time > nighttime_finish:
        schedule = "Daytime schedule on"
        send_request(channel, request_queue, f"{schedule}")

    channel.basic_consume(queue=response_queue, on_message_callback=receive_response, auto_ack=True)
    print(' [*] Waiting for response')
    channel.start_consuming()

def close_connection(connection):
    connection.close()


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    request_queue = 'schedule_energy_request'
    response_queue = 'schedule_energy_response'
    channel.queue_declare(queue=request_queue)
    channel.queue_declare(queue=response_queue)

    nighttime_start = 0
    nighttime_finish = 8
    current_time = 5

    try:
        make_decision(channel, request_queue, response_queue, nighttime_start, nighttime_finish, current_time)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        close_connection(connection)
