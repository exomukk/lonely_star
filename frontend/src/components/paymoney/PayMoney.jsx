// src/components/paymoney/PayMoney.jsx
import React, { useState } from 'react';
import './PayMoney.css';
import QRCode from 'qrcode';

const PayMoney = () => {
    const [amount, setAmount] = useState('');
    const [paymentMethod, setPaymentMethod] = useState('visa');
    const [showQR, setShowQR] = useState(false);
    const [qrCodeUrl, setQrCodeUrl] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Validate user input
        if (!amount || !paymentMethod) {
            alert('Vui lòng nhập đủ thông tin!');
            return;
        }

        try {
            // Prepare the data you want to encode in the QR
            // For example, it could be a payment URL, or just a string
            const dataToEncode = `Method=${paymentMethod}&Amount=${amount}`;

            // Generate QR code as a data URL
            const generatedUrl = await QRCode.toDataURL(dataToEncode);

            // Store the generated data URL in state
            setQrCodeUrl(generatedUrl);

            // Show the popup
            setShowQR(true);
        } catch (err) {
            console.error('Error generating QR code:', err);
        }
    };

    const handleClosePopup = () => {
        setShowQR(false);
    };

    return (
        <div className="paymoney-container">
            <div className="paymoney-card">
                <h1>Nạp tiền</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Số tiền:</label>
                        <input
                            type="number"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            placeholder="Nhập số tiền"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Phương thức thanh toán:</label>
                        <select
                            value={paymentMethod}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                        >
                            <option value="visa">Visa</option>
                            <option value="bank">Thẻ ngân hàng</option>
                            <option value="momo">Momo</option>
                            <option value="paypal">PayPal</option>
                        </select>
                    </div>
                    <button type="submit">Nạp tiền</button>
                </form>
            </div>

            {/* QR pop-up */}
            {showQR && (
                <div className="qr-popup-overlay">
                    <div className="qr-popup">
                        <span className="close-btn" onClick={handleClosePopup}>
                            &times;
                        </span>
                        <h2>Quét QR để thanh toán</h2>
                        {/* Use the data URL for the image source */}
                        <img src={qrCodeUrl} alt="Dynamic QR" />
                        <p>
                            Bạn đang nạp số tiền <strong>{amount}đ</strong> bằng phương thức{' '}
                            <strong>{paymentMethod}</strong>.
                        </p>
                        <p>Vui lòng quét mã để thanh toán.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PayMoney;
