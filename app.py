from flask import Flask, render_template, request, jsonify
import pagarme
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Configure Pagar.me with API key
pagarme.authentication_key(app.config['PAGARME_API_KEY'])

@app.route('/')
def index():
    """Render the main payment page"""
    return render_template('index.html')

@app.route('/add-card', methods=['POST'])
def add_card():
    """Endpoint to add a card to the wallet"""
    try:
        data = request.json
        card_hash = data['card_hash']
        customer_id = data.get('customer_id', 'temp_customer')

        # Create card in Pagar.me
        card = pagarme.card.create({
            'card_hash': card_hash,
            'customer_id': customer_id
        })

        return jsonify({
            "success": True, 
            "card_id": card['id'], 
            "message": "Card added successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/process-payment', methods=['POST'])
def process_payment():
    """Process payment with split rules"""
    try:
        data = request.json
        amount = int(data['amount'])  # Amount in cents
        card_id = data['card_id']
        customer_id = data.get('customer_id', 'temp_customer')
        
        # Hardcoded store recipient ID for example
        store_recipient_id = 'store_recipient_123'

        # Define split rules
        split_rules = [
            {
                'recipient_id': app.config['FASTLANE_RECIPIENT_ID'],
                'percentage': 5,
                'liable': True,
                'charge_processing_fee': False
            },
            {
                'recipient_id': store_recipient_id,
                'percentage': 95,
                'liable': True,
                'charge_processing_fee': True
            }
        ]

        # Create transaction
        transaction = pagarme.transaction.create({
            'amount': amount,
            'card_id': card_id,
            'customer': {'id': customer_id},
            'payment_method': 'credit_card',
            'split_rules': split_rules
        })

        return jsonify({
            "success": True, 
            "transaction": transaction,
            "message": "Payment processed successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Pagar.me webhook events"""
    try:
        event = request.json
        event_type = event.get('event', '')
        
        if event_type == 'transaction_status_changed':
            transaction = event['transaction']
            print(f"Transaction status: {transaction['status']}")
        
        return '', 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)