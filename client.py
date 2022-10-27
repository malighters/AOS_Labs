import socket
import logging

HOST = '127.0.0.1'
PORT = 1025+18


class Client:

    def __init__(self):
        try:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            logging.getLogger("Client")
            logging.basicConfig(filename="myClient.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info('Client started.')

            sock.connect((HOST, PORT))
            logging.info("Connected to a server.")
            while True:
                data = sock.recv(256).decode('utf-8')
                print(data)
                if data.__contains__("to stop the program"):
                    break
            logging.info('Got welcome message.')
            while True:
                data = input('Send request:\n')
                sock.send(data.encode('utf-8'))
                logging.info('Sent request: ' + data)
                data = sock.recv(256).decode('utf-8')
                logging.info('Received message: ' + data)
                print('Answer: ', data)
                if 'Stop' in data or 'STOP' in data:
                    sock.close()
                    logging.info("End of session")
                    break
            print('Connection closed.')
            logging.info('Connection closed.')
        except Exception as e:
            print(f'Happened exception: {e}')
            logging.info('Caught an error. Closing connection.')

    @staticmethod
    def reconnect():
        while True:
            answer = input("Do you want to try to reconnect? Y/n: ")
            if answer.lower() in 'yn':
                break
        if answer.lower() == 'y':
            return True
        else:
            return False


def main():
    client = Client()


if __name__ == "__main__":
    main()
