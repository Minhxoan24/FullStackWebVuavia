from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))  # Cần ép kiểu về int nếu dùng số
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 10080))

# CassoFlow 
CASSO_CLIENT_ID = os.getenv("CLIENT_ID")
CASSO_API_KEY = os.getenv("API_KEY")
CASSO_CHECKSUM_KEY = os.getenv("CHECKSUM_KEY")  # Đây là webhook secret
CASSO_BANK_ACCOUNT_NAME = os.getenv("CASSO_BANK_ACCOUNT_NAME")
CASSO_BANK_NAME = os.getenv("CASSO_BANK_NAME")
# Bạn cần thêm CASSO_BANK_ACCOUNT_ID nếu chưa có (lấy từ Casso dashboard)
CASSO_BANK_ACCOUNT_ID = os.getenv("CASSO_BANK_ACCOUNT_ID")  

# Email Configuration
SMTP_HOST= os.getenv("SMTP_HOST")
SMTP_PORT=int(os.getenv("SMTP_PORT", 587))
SMTP_USER=os.getenv("SMTP_USER")
SMTP_PASS=os.getenv("SMTP_PASS")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")