from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# RxAI app config
BASE_URL = os.getenv("RXAI_URL")
USERNAME = os.getenv("RXAI_USER")
PASSWORD = os.getenv("RXAI_PASSWORD")

# Paths
OUTPUT_DIR = "outputs"
PRESCRIPTION_DIR = "prescriptions"