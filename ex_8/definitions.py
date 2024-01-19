from dotenv import load_dotenv
import os

load_dotenv()

DB_CONNECTION_STRING = f"{os.getenv('DB_ENGINE')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_DOMAIN')}/{os.getenv('DB_NAME')}?retryWrites=true&w=majority"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
