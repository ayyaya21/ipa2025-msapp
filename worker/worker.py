import os
from dotenv import load_dotenv
from consumer import consume

load_dotenv()

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")

consume(RABBITMQ_HOST)
