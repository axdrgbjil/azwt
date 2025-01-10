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
    # Generate a valid credit card number using the Luhn algorithm
    card_number = random.randint(1000000000000000, 9999999999999999)
    while not validate_credit_card(card_number):
        card_number = random.randint(1000000000000000, 9999999999999999)
    return card_number

# Function to generate a random invalid credit card number
def generate_invalid_credit_card():
    card_number = random.randint(1000000000000000, 9999999999999999)
    # Intentionally modify the card to make it invalid
    card_number += random.randint(1, 9)  # Slight modification to make it invalid
    return card_number

# Generate 500 credit card numbers with 80% valid and 20% invalid
credit_cards = []
for _ in range(400):  # 80% valid
    credit_cards.append(generate_valid_credit_card())

for _ in range(100):  # 20% invalid
    credit_cards.append(generate_invalid_credit_card())

# Shuffle the list of credit cards to randomize the valid/invalid distribution
random.shuffle(credit_cards)

# TCP server setup
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345  # Port to listen on

def start_game(client_socket):
    # Send welcome message to the client
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

            # Check if the user gives the correct answer
            if (valid and answer == 'yes') or (not valid and answer == 'no'):
                correct_answers += 1
                client_socket.sendall(b"Correct!\n\n")
            else:
                client_socket.sendall(b"Incorrect answer! Game over.\n")
                client_socket.sendall(f"You failed at card {i}\nGoodbye.\n".encode())
                break

            # If the user has passed all 500 questions, show the flag
            if correct_answers == 500:
                client_socket.sendall(b"Congratulations! You answered all questions correctly!\n")
                client_socket.sendall(b"Flag: FLAG{credit_card_master}\n")
                break

        except ConnectionResetError:
            print("Connection was reset by the client. Exiting game.")
            client_socket.sendall(b"Connection was reset by the client. Game over.\n")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_socket.sendall(b"An unexpected error occurred. Game over.\n")
            break

    client_socket.close()

# Start the server to listen for incoming connections
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}...")

    while True:
        try:
            # Accept a new connection from a client
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Start the game with the connected client
            start_game(client_socket)
        
        except Exception as e:
            print(f"Error accepting new connection: {e}")

if __name__ == "__main__":
    start_server()