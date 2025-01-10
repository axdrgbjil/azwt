import random
import time
import socket

# Function to simulate credit card validation using Luhn's algorithm
def validate_credit_card(card_number):
    def luhn_check(card_number):
        card_number = [int(x) for x in str(card_number)]
        check_sum = 0
        reverse_digits = card_number[::-1]
        for i, digit in enumerate(reverse_digits):
            if i % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            check_sum += digit
        return check_sum % 10 == 0

    return luhn_check(card_number)

# Function to generate a random valid credit card number
def generate_valid_credit_card():
    card_number = random.randint(1000000000000000, 9999999999999999)
    while not validate_credit_card(card_number):
        card_number = random.randint(1000000000000000, 9999999999999999)
    return card_number

# Function to generate a random invalid credit card number
def generate_invalid_credit_card():
    card_number = random.randint(1000000000000000, 9999999999999999)
    card_number += random.randint(1, 9)
    return card_number

# Generate 500 credit card numbers with 80% valid and 20% invalid
credit_cards = []
for _ in range(400):  
    credit_cards.append(generate_valid_credit_card())

for _ in range(100):  
    credit_cards.append(generate_invalid_credit_card())

random.shuffle(credit_cards)

# TCP server setup
HOST = '0.0.0.0'  
PORT = 12345  

def start_game(client_socket):
    try:
        client_socket.sendall(b"Welcome to the Credit Card Validation Game!\n")
        client_socket.sendall(b"You will be given 500 credit card numbers.\n")
        client_socket.sendall(b"For each number, type 'yes' if it is valid, or 'no' if it is not.\n")
        client_socket.sendall(b"If you get all answers correct, you will win the flag!\n")
        client_socket.sendall(b"Let's get started!\n\n")
        time.sleep(2)
    
        correct_answers = 0
        for i, card in enumerate(credit_cards, 1):
            valid = validate_credit_card(card)
            client_socket.sendall(f"Credit Card {i}: {card}\n".encode())
            client_socket.sendall(b"Is this card valid? (yes/no): ")

            try:
                # Receive the answer from the client
                answer = client_socket.recv(1024).decode().strip().lower()

                if not answer:
                    client_socket.sendall(b"Connection closed or no answer. Game over.\n")
                    break

                if (valid and answer == 'yes') or (not valid and answer == 'no'):
                    correct_answers += 1
                    client_socket.sendall(b"Correct!\n\n")
                else:
                    client_socket.sendall(b"Incorrect answer! Game over.\n")
                    client_socket.sendall(f"You failed at card {i}\nGoodbye.\n".encode())
                    break

                if correct_answers == 500:
                    client_socket.sendall(b"Congratulations! You answered all questions correctly!\n")
                    client_socket.sendall(b"Flag: FLAG{credit_card_master}\n")
                    break

            except ConnectionResetError:
                print("Connection reset by client.")
                client_socket.sendall(b"Connection reset by client. Game over.\n")
                break
            except socket.error as e:
                print(f"Socket error: {e}")
                client_socket.sendall(b"A socket error occurred. Game over.\n")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                client_socket.sendall(b"An unexpected error occurred. Game over.\n")
                break

        client_socket.close()
    except socket.error as e:
        print(f"Error in game loop: {e}")
        client_socket.sendall(b"Game loop error. Closing connection.\n")
        client_socket.close()

# Start the server to listen for incoming connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            start_game(client_socket)
        
        except Exception as e:
            print(f"Error accepting new connection: {e}")

if __name__ == "__main__":
    start_server()
