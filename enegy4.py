import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='security_energy')

    block = False
    alarm = False

    def callback(ch, method, properties, security):
        decoded_message = security.decode('utf-8')
        print(f" [x] Received security massage: {decoded_message}")
        nonlocal alarm, block
        if decoded_message == "Invasion detected":
            block = True
            alarm = True
            print("Decision: Doors are locked")
        elif decoded_message == "Smoke detected":
            alarm = True
            print("Decision: Electricity off")
        else:
            print("everything ok")



    channel.basic_consume(queue='security_energy', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages')

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)