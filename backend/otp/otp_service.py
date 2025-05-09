import random, time
from flask import current_app
from flask_mail import Message

# in‐memory store
otp_store = {}
OTP_TTL = 5 * 60

def generate_otp():
    return f"{random.randint(0, 999999):06d}"

def store_otp(email, code):
    otp_store[email] = (code, time.time() + OTP_TTL)

def verify_otp(email, code):
    record = otp_store.get(email)
    if not record:
        return False, "Chưa gửi hoặc đã hết hạn"
    real, expires = record
    if time.time() > expires:
        otp_store.pop(email, None)
        return False, "OTP đã hết hạn"
    if code != real:
        return False, "OTP không đúng"
    otp_store.pop(email, None)
    return True, None

def send_otp_mail(email, code):
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