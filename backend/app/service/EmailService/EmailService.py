import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime
import logging

# Import config values
from app.core.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Sử dụng config từ config.py thay vì os.getenv trực tiếp
        self.smtp_server = SMTP_HOST or "smtp.gmail.com"
        self.smtp_port = SMTP_PORT or 587
        self.email_address = SMTP_USER
        self.email_password = SMTP_PASS
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Validate configuration
        if not self.email_address or not self.email_password:
            logger.error("Email configuration incomplete: SMTP_USER or SMTP_PASS not set")
            raise ValueError("Email service not configured properly. Check SMTP_USER and SMTP_PASS in environment variables.")
        
        logger.info(f"EmailService initialized with SMTP server: {self.smtp_server}:{self.smtp_port}")

    def _create_otp_text_message(self, otp: str, email: str) -> str:
        """Tạo text message đơn giản cho OTP"""
        message = f"""
VUAVIA - MÃ XÁC THỰC OTP

Xin chào!

Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản: {email}

Mã OTP của bạn là: {otp}

Thông tin quan trọng:
- Mã OTP có 6 chữ số
- Có hiệu lực trong 3 phút
- Tối đa 5 lần nhập sai
- Chỉ sử dụng một lần

LưU Ý BẢO MẬT:
Không chia sẻ mã này với bất kỳ ai. Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.

Thời gian gửi: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

---
Vuavia System
Email này được gửi tự động, vui lòng không trả lời.
        """
        return message.strip()

    def _send_email_sync(self, to_email: str, subject: str, message: str) -> bool:
        """Gửi email đồng bộ với plain text"""
        try:
            logger.info(f"Attempting to send email to: {to_email}")
            
            # Tạo message đơn giản
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = subject

            # Gửi email với detailed error handling
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                logger.debug(f"SMTP connection established to {self.smtp_server}:{self.smtp_port}")
                
                server.login(self.email_address, self.email_password)
                logger.debug("SMTP authentication successful")
                
                server.send_message(msg)
                logger.info(f"Email sent successfully to: {to_email}")
                
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            logger.error("Check SMTP_USER and SMTP_PASS credentials")
            return False
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Recipients refused: {str(e)}")
            return False
        except smtplib.SMTPServerDisconnected as e:
            logger.error(f"SMTP server disconnected: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending email: {str(e)}")
            logger.error(f"Email config - Server: {self.smtp_server}, Port: {self.smtp_port}, User: {self.email_address}")
            return False

    async def send_otp_email(self, email: str, otp: str) -> bool:
        """Gửi email OTP bất đồng bộ với plain text"""
        try:
            subject = "VUAVIA - Mã OTP đặt lại mật khẩu"
            message = self._create_otp_text_message(otp, email)
            
            # Chạy gửi email trong thread pool để không block
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._send_email_sync, 
                email, 
                subject, 
                message
            )
            
            if not result:
                logger.error(f"Failed to send OTP email to: {email}")
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to send OTP email. Please check email service configuration."
                )
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in send_otp_email: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to send OTP email: {str(e)}"
            )

    async def send_password_reset_success_email(self, email: str) -> bool:
        """Gửi email thông báo đặt lại mật khẩu thành công với plain text"""
        try:
            subject = "VUAVIA - Đặt lại mật khẩu thành công"
            
            message = f"""
VUAVIA - ĐẶT LẠI MẬT KHẨU THÀNH CÔNG

Chúc mừng!

Mật khẩu cho tài khoản {email} đã được đặt lại thành công.

Bạn có thể đăng nhập bằng mật khẩu mới ngay bây giờ.

BẢO MẬT TÀI KHOẢN:
- Không chia sẻ mật khẩu với bất kỳ ai
- Sử dụng mật khẩu mạnh và duy nhất  
- Đăng xuất khỏi các thiết bị không tin cậy

Nếu bạn không thực hiện thay đổi này, vui lòng liên hệ hỗ trợ ngay lập tức.

Thời gian: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

---
Vuavia System  
Email này được gửi tự động, vui lòng không trả lời.
            """
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._send_email_sync, 
                email, 
                subject, 
                message.strip()
            )
            
            if not result:
                logger.warning(f"Failed to send success notification email to: {email}")
            
            return result
            
        except Exception as e:
            # Log error nhưng không raise exception vì đây không phải critical
            logger.error(f"Failed to send success email to {email}: {str(e)}")
            return False

    def __del__(self):
        """Cleanup executor khi object bị destroy"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)

# Khởi tạo EmailService
email_service = EmailService()