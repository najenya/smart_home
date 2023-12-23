import pika


def callback(ch, method, properties, body):
    decoded_message = body.decode('utf-8')
    print(f" [x] Received Request: {decoded_message}")
    result = adjust_energy_consumption(decoded_message)
    send_response(channel, result)


def adjust_energy_consumption(schedule):
    global current_temperature
    global optimal_temperature
    global is_turnon
    result = ""
    if current_temperature > optimal_temperature and schedule == "Cool down":
        if is_turnon is False:
            result = "Decision: Turn on the conditioner"
            is_turnon = True
        else:
            result = "Conditioner is working"
        current_temperature -= 1
    elif current_temperature < optimal_temperature and schedule == "Heat up":
        if is_turnon is False:
            result = "Decision: Turn on the heating"
            is_turnon = True
        else:
            result = "Heating is working"
        current_temperature += 1
    else:
        if is_turnon is True:
            result = "Decision: Turn off"
        else:
            result = "No change"
    return result


def send_response(channel, response):
    channel.basic_publish(exchange='', routing_key=response_queue, body=response)
    print(" [x] Sent Response:", response)


def start_consuming(channel, request_queue):
    print(' [*] Waiting for requests')
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

    current_temperature = 25
    optimal_temperature = 22
    is_turnon = False

    try:
        channel.basic_consume(queue=request_queue, on_message_callback=callback, auto_ack=True)
        start_consuming(channel, request_queue)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        close_connection(connection)
