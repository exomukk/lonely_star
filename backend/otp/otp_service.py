import random, time
from flask import current_app
from flask_mail import Message

# in‐memory store

class OTPService:
    def __init__(self):
        self.otp_store = {}
        self.OTP_TTL = 5 * 60

    def generate_otp(self):
        return f"{random.randint(0, 999999):06d}"

    def store_otp(self,email, code):
        self.otp_store[email] = (code, time.time() + self.OTP_TTL)

    def verify_otp(self,email, code):
        print("verify-otp: ",email, code)
        record = self.otp_store.get(email)
        print(record)
        if not record:
            print('Verify OTP: Chưa gửi hoặc đã hết hạn')
            return False, "Chưa gửi hoặc đã hết hạn"
        real, expires = record
        if time.time() > expires:
            print('Verify OTP: đã hết hạn')
            self.otp_store.pop(email, None)
            return False, "OTP đã hết hạn"
        if code != real:
            print('Verify OTP: Sai')
            return False, "OTP không đúng"
        self.otp_store.pop(email, None)
        return True, None

    def send_otp_mail(self,email, code):
        # Tạo Message
        msg = Message(
            subject="[YourApp] OTP Verification",
            recipients=[email],
            body=f"Mã OTP của bạn là {code}. Hết hạn sau 5 phút."
        )
        # Lấy instance Mail đã đăng ký trong current_app
        mail = current_app.extensions.get('mail')
        if not mail:
            raise RuntimeError("Flask-Mail chưa được khởi tạo")
        mail.send(msg)

otp_service = OTPService()