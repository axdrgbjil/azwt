import random
import time
import socket
import signal
import sys

# Your existing credit card validation functions remain the same
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

def generate_valid_credit_card():
    card_number = random.randint(1000000000000000, 9999999999999999)
    while not validate_credit_card(card_number):
        card_number = random.randint(1000000000000000, 9999999999999999)
    return card_number

def generate_invalid_credit_card():
    card_number = random.randint(1000000000000000, 9999999999999999)
    card_number += random.randint(1, 9)
    return card_number

# Generate credit cards once at startup
credit_cards = []
for _ in range(400):  
    credit_cards.append(generate_valid_credit_card())
for _ in range(100):  
    credit_cards.append(generate_invalid_credit_card())
random.shuffle(credit_cards)

def handle_client(client_socket, address):
    """Handle a single client connection"""
    print(f"New connection from {address}")
    try:
        client_socket.settimeout(30)  # 30 second timeout
        welcome_message = (
            "Welcome to the Credit Card Validation Game!\n"
            "You will be given 500 credit card numbers.\n"
            "For each number, type 'yes' if it is valid, or 'no' if it is not.\n"
            "If you get all answers correct, you will win the flag!\n"
            "Let's get started!\n\n"
        )
        client_socket.sendall(welcome_message.encode())
        
        correct_answers = 0
        for i, card in enumerate(credit_cards, 1):
            valid = validate_credit_card(card)
            client_socket.sendall(f"Credit Card {i}: {card}\n".encode())
            client_socket.sendall(b"Is this card valid? (yes/no): ")
            
            try:
                answer = client_socket.recv(1024).decode().strip().lower()
                if not answer:
                    raise ConnectionError("Empty response received")
                
                if (valid and answer == 'yes') or (not valid and answer == 'no'):
                    correct_answers += 1
                    client_socket.sendall(b"Correct!\n\n")
                else:
                    client_socket.sendall(f"Incorrect answer! Game over.\nYou failed at card {i}\nGoodbye.\n".encode())
                    break

                if correct_answers == 500:
                    client_socket.sendall(b"Congratulations! You answered all questions correctly!\n")
                    client_socket.sendall(b"Flag: FLAG{credit_card_master}\n")
                    break

            except socket.timeout:
                client_socket.sendall(b"Timeout reached. Game over.\n")
                break
                
    except (ConnectionResetError, BrokenPipeError) as e:
        print(f"Connection error with {address}: {e}")
    except Exception as e:
        print(f"Unexpected error with {address}: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass
        print(f"Connection closed with {address}")

def start_server(host='0.0.0.0', port=12345):
    """Start the server with proper signal handling and error recovery"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def signal_handler(sig, frame):
        print("\nShutting down server...")
        try:
            server_socket.close()
        except:
            pass
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}...")
        
        while True:
            try:
                client_socket, address = server_socket.accept()
                handle_client(client_socket, address)
            except Exception as e:
                print(f"Error accepting connection: {e}")
                continue
                
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
