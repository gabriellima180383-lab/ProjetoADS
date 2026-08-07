import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

APP_NAME = "GL Secure Manager"
VERSION = "1.0.0"

DATABASE_DIR = os.path.join(BASE_DIR, "database")

os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATABASE_DIR, "gl_secure_manager.db")

DEBUG = True
