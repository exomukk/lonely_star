# otp/routes.py
from flask import Blueprint, request, jsonify
from otp.otp_service import otp_service

otp_bp = Blueprint('otp', __name__, url_prefix='/otp')
otp_service = otp_service()
@otp_bp.route('/resend-otp', methods=['POST'])
def resend():
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email bắt buộc"}), 400

    code = otp_service.generate_otp()
    otp_service.store_otp(email, code)
    try:
        otp_service.send_otp_mail(email, code)
        return jsonify({"message": "Đã gửi OTP"}), 200
    except Exception as e:
        return jsonify({"message": "Gửi OTP thất bại"}), 500

@otp_bp.route('/verify-otp', methods=['POST'])
def verify():
    data = request.get_json() or {}
    email = data.get('email')
    code  = data.get('otp')
    ok, msg = otp_service.verify_otp(email, code)
    if ok:
        return jsonify({"message": "Xác thực thành công"}), 200
    return jsonify({"message": msg}), 400