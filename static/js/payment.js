document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('payment-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        messageDiv.innerHTML = '';

        const cardNumber = document.getElementById('card-number').value;
        const cardExpiry = document.getElementById('card-expiry').value;
        const cardCVV = document.getElementById('card-cvv').value;
        const amount = document.getElementById('payment-amount').value;

        // Validate inputs
        if (!cardNumber || !cardExpiry || !cardCVV || !amount) {
            showMessage('Please fill in all fields', 'text-red-500');
            return;
        }

        try {
            // Generate card hash using Pagar.me
            const cardHash = await generateCardHash(cardNumber, cardExpiry, cardCVV);
            
            // Add card to wallet
            const addCardResponse = await fetch('/add-card', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    card_hash: cardHash,
                    customer_id: 'user_' + Date.now()  // Generate a unique ID
                })
            });

            const addCardResult = await addCardResponse.json();
            
            if (!addCardResult.success) {
                throw new Error(addCardResult.error);
            }

            // Process payment
            const paymentResponse = await fetch('/process-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    amount: Math.round(parseFloat(amount) * 100),  // Convert to cents
                    card_id: addCardResult.card_id,
                    customer_id: 'user_' + Date.now()
                })
            });

            const paymentResult = await paymentResponse.json();

            if (paymentResult.success) {
                showMessage('Payment processed successfully!', 'text-green-500');
            } else {
                throw new Error(paymentResult.error);
            }

        } catch (error) {
            showMessage(`Error: ${error.message}`, 'text-red-500');
        }
    });

    function generateCardHash(number, expiry, cvv) {
        return new Promise((resolve, reject) => {
            const [month, year] = expiry.split('/');
            pagarme.createCardHash({
                card: {
                    number: number.replace(/\s/g, ''),
                    holderName: 'Test User',
                    expirationMonth: month,
                    expirationYear: year,
                    cvv: cvv
                }
            }, (error, cardHash) => {
                if (error) reject(error);
                else resolve(cardHash);
            });
        });
    }

    function showMessage(message, className) {
        messageDiv.innerHTML = message;
        messageDiv.className = `text-center ${className}`;
    }
});