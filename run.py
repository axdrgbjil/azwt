import os
from flask import Flask, request, Response, stream_with_context
import random
import time

app = Flask(__name__)

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

# Generate credit cards
credit_cards = []
for _ in range(400):  
    credit_cards.append(generate_valid_credit_card())
for _ in range(100):  
    credit_cards.append(generate_invalid_credit_card())
random.shuffle(credit_cards)

@app.route('/')
def home():
    return '''
    <html>
        <body>
            <h1>Credit Card Validation Game</h1>
            <p>To play:</p>
            <ol>
                <li>GET /play to start the game and receive a card number</li>
                <li>POST /play with answer="yes" or "no" and card_number=XXXXX to submit your answer</li>
            </ol>
        </body>
    </html>
    '''

def generate_game():
    yield "Welcome to the Credit Card Validation Game!\n"
    yield "You will be given 500 credit card numbers.\n"
    yield "For each number, send a POST request with 'yes' if it is valid, or 'no' if it is not.\n"
    yield "If you get all answers correct, you will win the flag!\n\n"
    
    correct_answers = 0
    for i, card in enumerate(credit_cards, 1):
        valid = validate_credit_card(card)
        yield f"Credit Card {i}: {card}\n"
        
        # Wait for answer through POST request
        yield f"WAITING_FOR_ANSWER\n"  # Special marker
        break  # Only send first card initially

@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        return Response(stream_with_context(generate_game()), mimetype='text/plain')
    
    elif request.method == 'POST':
        answer = request.form.get('answer', '').strip().lower()
        card_number = int(request.form.get('card_number', 0))
        
        if not card_number or answer not in ['yes', 'no']:
            return "Invalid input. Send 'answer' and 'card_number' in the POST request.", 400
        
        valid = validate_credit_card(card_number)
        if (valid and answer == 'yes') or (not valid and answer == 'no'):
            return "Correct! Next card coming up...", 200
        else:
            return "Incorrect! Game over.", 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
