import pika


def callback(ch, method, properties, body):
    decoded_message = body.decode('utf-8')
    print(f" [x] Received Request: {decoded_message}")
    result = adjust_energy_consumption(decoded_message)
    send_response(channel, result)


def adjust_energy_consumption(schedule):
    global current_energy_consumption
    global is_turnon
    result = ""
    if schedule == "Night mode on":
        if is_turnon is True:
            current_energy_consumption -= 200
            result = "Decision: Switch off devices " + "current consumption = " + str(current_energy_consumption)
            is_turnon = False
        else:
            result = "Low power consumption"
    else:
        if is_turnon is False:
            current_energy_consumption += 200
            result = "Decision: Switch on devices " + "current consumption = " + str(current_energy_consumption)
            is_turnon = True
        else:
            result = "Standart electricity consumption: " + str(current_energy_consumption)
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
    request_queue = 'schedule_energy_request'
    response_queue = 'schedule_energy_response'
    channel.queue_declare(queue=request_queue)
    channel.queue_declare(queue=response_queue)

    current_energy_consumption = 700
    is_turnon = True

    try:
        channel.basic_consume(queue=request_queue, on_message_callback=callback, auto_ack=True)
        start_consuming(channel, request_queue)
    except KeyboardInterrupt:
        print('Interrupted')
    finally:
        close_connection(connection)
