# Configuration settings for Fastlane Wallet

class Config:
    # Replace these with your actual Pagar.me credentials
    PAGARME_API_KEY = 'test_your_test_api_key'
    
    # Placeholder IDs - replace with real Pagar.me recipient IDs
    FASTLANE_RECIPIENT_ID = 'fastlane_recipient_id'
    
    # Flask secret key for sessions and CSRF protection
    SECRET_KEY = 'your_very_secret_and_random_key'
    
    # Database configuration (if using a database)
    DATABASE_URI = 'sqlite:///fastlane_wallet.db'

# Different configurations for development and production
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False