import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "w019bf5f.kasserver.com"),
    "user": os.getenv("DB_USER", "d042e0c3"),
    "password": os.getenv("DB_PASSWORD", "mwzMmhjW4GsmJUJamYyj"),
    "database": os.getenv("DB_NAME", "d042e0c3"),
    'port': 3306,  # Default MySQL port
    # 'SQLALCHEMY_DATABASE_URI': "mysql+mysqlconnector://d042e0c3:mwzMmhjW4GsmJUJamYyj@w019bf5f.kasserver.com/d042e0c3",
}
