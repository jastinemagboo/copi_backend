import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print out the DATABASE_URL to check if it is being loaded correctly
print("DATABASE_URL:", os.getenv('DATABASE_URL'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
