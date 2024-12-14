import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # General configurations
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # LinkedIn configurations
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI')

    # Facebook configurations
    FACEBOOK_CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET')
    FACEBOOK_REDIRECT_URI = os.getenv('FACEBOOK_REDIRECT_URI')
    
   

class DevelopmentConfig(Config):
    DEBUG = True
    # Other development-specific configurations

class ProductionConfig(Config):
    DEBUG = False
    # Other production-specific configurations

# If you are using Flask's `from_object` to load configurations, you would use:
# app.config.from_object('config.DevelopmentConfig')

