import pika

def send_request(channel, request_queue, request):
    channel.basic_publish(exchange='', routing_key=request_queue, body=request)
    print(" [x] Sent Request:", request)

def receive_response(ch, method, properties, body):
    decoded_message = body.decode('utf-8')
    print(f" [x] Received Response: {decoded_message}")

def make_decision(channel, request_queue, response_queue, current_time, schedule_start, schedule_finish, switch):
    if current_time >= schedule_start and current_time <= schedule_finish:
        while current_time < schedule_finish:
            if switch == "Cool down":
                schedule = "Cool down"
            else:
                schedule = "Heat up"
            send_request(channel, request_queue, f"{schedule}")
            current_time += 1
        if current_time == schedule_finish:
            schedule = "Finish schedule"
            send_request(channel, request_queue, f"{schedule}")
    if current_time < schedule_start or current_time > schedule_finish:
        schedule = "The schedule is set for a different time"
        send_request(channel, request_queue, f"{schedule}")

    channel.basic_consume(queue=response_queue, on_message_callback=receive_response, auto_ack=True)
    print(' [*] Waiting for response')
    channel.start_consuming()

def close_connection(connection):
    connection.close()


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    request_queue = 'schedule_climate_request'
    response_queue = 'schedule_climate_response'
    channel.queue_declare(queue=request_queue)
    channel.queue_declare(queue=response_queue)

    # с 14-16 охлаждение (Cool down), (нагрев - Heat up)
    current_time = 14
    schedule_start = 14
    schedule_finish = 16
    switch = "Cool down"

    try:
        make_decision(channel, request_queue, response_queue, current_time, schedule_start, schedule_finish, switch)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        close_connection(connection)
