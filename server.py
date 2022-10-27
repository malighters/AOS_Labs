import socket
import random
import logging


def generateNewNumber():
    s = ""
    while len(s) != 4:
        s1 = str(random.randint(0, 10))
        if s1 not in s:
            s += s1
    print("Random number: " + s)
    return s


class Server:
    def __init__(self):

        try:

            HOST = '127.0.0.1'
            PORT = 1025 + 18
            utf = 'utf-8'

            logging.getLogger("Server")
            logging.basicConfig(filename="myServer.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info("Server started")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            counter = 0

            try:
                sock.bind((HOST, PORT))
            except OSError:
                print("Host is used.")
                logging.warning("HOST IS USED. ")
                exit()
            sock.listen(1)
            connection, client_address = sock.accept()

            print("Connected:", client_address)
            logging.info("Connected to a client. ")

            for sentence in self.welcome_message():
                connection.send(sentence.encode(utf))
            logging.info("Sent a welcome message.")

            print("Listening")
            logging.info('Listening to a client.')
            isActiveGame = False
            try:
                while True:
                    data = connection.recv(256).decode(utf)
                    logging.info(f'Received message: {data}')
                    print(data)
                    if not data:
                        break
                    if data == "new_game":
                        if isActiveGame:
                            results = "You haven't finished previous game"
                        else:
                            rand_num = generateNewNumber()
                            isActiveGame = True
                            results = "Please enter your number"
                            logging.info("Start of a new game ")
                    elif data == "end_game":
                        if isActiveGame:
                            isActiveGame = False
                            results = "The number was " + rand_num
                            logging.info("User ended a game ")
                        else:
                            results = "The game hasn't been started"
                    elif data == "end_session":
                        if isActiveGame:
                            results = "The number was " + rand_num + ". Stop"
                        else:
                            results = "Stop"
                            connection.send(results.encode(utf))
                            logging.info("Sent message: " + results)
                        logging.info("The end of session")
                        break
                    elif data.__contains__("random") and isActiveGame:
                        rand = generateNewNumber();
                        answer1, answer2, counter = self.process(rand, rand_num, counter)
                        if answer1 is None or answer2 is None:
                            logging.info("Process function broke at some moment.")
                            raise IOError
                        if (answer1, answer2) == (4, 4):
                            results = "Congratulations! You needed " + str(
                                counter) + " iterations to guess the " + str(rand_num)
                            isActiveGame = False
                        else:
                            results = "Random number is " + str(rand) + '\n' + str(answer1) + " " + str(answer2)
                    elif data == "who":
                        results = self.whoami()
                    elif data.isnumeric() and len(data) == 4 and isActiveGame:
                        answer1, answer2, counter = self.process(data, rand_num, counter)
                        if answer1 is None or answer2 is None:
                            logging.info("Process function broke at some moment.")
                            raise IOError
                        if (answer1, answer2) == (4, 4):
                            results = "Congratulations! You needed " + str(counter) + " iterations to guess the " + str(rand_num)
                            isActiveGame = False
                        else:
                            results = str(answer1) + " " + str(answer2)
                    else:
                        results = "Unknown command, please try again"
                    connection.send(results.encode(utf))
                    logging.info("Sent message: " + results)
            except:
                print("ERROR.")
                sock.send("STOP".encode(utf))
                logging.error("Caught en error. Closing connection.")
        finally:
            try:
                sock.close()
            except Exception as e:
                print(f' !Exception {e}')
                logging.warning(f'{e}')
            print("Connection closed.")

    def process(self, data: str, rand_number: str, count: int):
        try:
            counter1 = 0
            counter2 = 0
            for a in data:
                if a in rand_number:
                    counter1 += rand_number.count(a)

            l1 = list(data)
            l0 = list(rand_number)
            for i in range(0, 4):
                if l1[i] == l0[i]:
                    counter2 += 1
            count += 1
            return counter1, counter2, count

        except Exception as e:
            return f"={e}"

    def welcome_message(self):
        welcome = [
            "HI! It's a game where you need to guess the random number.",
            "When you send the random number you will get two numbers like an answer, the 1st num is how much correct",
            "numbers there are, and the 2nd one is how much nums are on correct place.",
            "Remember that all nums are unique, there can't be the same nums.",
            "Press 'new_game' to start, 'end_game' to stop game, and 'end_session' to stop the program. "
        ]
        return welcome

    def whoami(self):
        who = 'Chernenko Yevhenii, K-26, Game "Guess the number", №18'
        return who


def main():
    root = Server()


if __name__ == "__main__":
    main()
