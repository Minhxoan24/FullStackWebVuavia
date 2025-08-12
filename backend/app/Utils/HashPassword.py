import bcrypt 
def hash_password (password : str ) -> str:
   salt = bcrypt.gensalt() 
   hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Mã hóa mật khẩu bằng bcrypt
   return hashed.decode('utf-8')  # Trả về mật khẩu đã mã hóa dưới dạng chuỗi
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))  # Kiểm tra mật khẩu đã mã hóa với mật khẩu gốc