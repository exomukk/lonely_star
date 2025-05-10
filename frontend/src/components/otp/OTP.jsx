import React, { useState, useEffect } from 'react';
import './OTP.css';

const OTP = ({ email, onVerifySuccess, onClose }) => {
    const [otp, setOtp] = useState('');
    const [error, setError] = useState('');
    const [timer, setTimer] = useState(180);       // 3 phút = 180 giây
    const [resendDisabled, setResendDisabled] = useState(true);

    // Thiết lập countdown
    useEffect(() => {
        if (timer <= 0) return;
        const id = setInterval(() => setTimer(t => t - 1), 1000);
        return () => clearInterval(id);
    }, [timer]);

    // Khi hết 3 phút, cho phép gửi lại và thông báo
    useEffect(() => {
        if (timer === 0) {
            setResendDisabled(false);
        }
    }, [timer]);

    const formatTime = (sec) => {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
    };

    const handleVerify = async () => {
        console.log(`${process.env.REACT_APP_REACT_APP_API_BASE_URL}/otp/verify-otp`)
        try {
            const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/otp/verify-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, code: otp })
            });
            const data = await res.json();
            if (res.ok) {
                onVerifySuccess();
            } else {
                setError(data.message || 'Mã OTP không đúng, vui lòng thử lại.');
            }
        } catch (err) {
            setError('Lỗi mạng, vui lòng thử lại.');
        }
    };

    const handleResend = async () => {
        try {
            const res = await fetch('https://scamclubbe.creammjnk.uk/resend-otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            if (res.ok) {
                setTimer(180);
                setResendDisabled(true);
                setError('');
            } else {
                const data = await res.json();
                setError(data.message || 'Không thể gửi lại OTP.');
            }
        } catch {
            setError('Lỗi mạng, vui lòng thử lại.');
        }
    };

    return (
        <div className="otp-modal-backdrop">
            <div className="otp-modal">
                <h3>Nhập mã OTP</h3>
                {error && <p className="error">{error}</p>}
                <p>Chúng tôi đã gửi 1 mã 6 chữ số vào email: <b>{email}</b></p>
                <input
                    type="text"
                    maxLength="6"
                    value={otp}
                    onChange={e => setOtp(e.target.value.replace(/\D/, ''))}
                    placeholder="______"
                />
                <div className="timer">Thời gian còn: {formatTime(timer)}</div>
                <button onClick={handleVerify}>Xác thực OTP</button>
                <button onClick={handleResend} disabled={resendDisabled}>
                    {resendDisabled ? `Gửi lại sau (${formatTime(timer)})` : 'Gửi lại OTP'}
                </button>
                <button className="close-btn" onClick={onClose}>Hủy</button>
            </div>
        </div>
    );
};

export default OTP;
