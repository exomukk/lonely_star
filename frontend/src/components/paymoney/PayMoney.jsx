// src/components/paymoney/PayMoney.jsx
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import QRCode from 'qrcode';
import './PayMoney.css';

const PayMoney = () => {
  const [amount, setAmount] = useState('');
  const [method, setMethod] = useState('visa');

  // state chung cho popup
  const [popupType, setPopupType] = useState(null);
  const [transactionId, setTransactionId] = useState(null);
  const [qrUrl, setQrUrl] = useState('');
  const [approvalUrl, setApprovalUrl] = useState('');
  const [status, setStatus] = useState('pending');

  // visa form state
  const [cardNumber, setCardNumber] = useState('');
  const [cardName, setCardName] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvv, setCvv] = useState('');

  const pollingRef = useRef(null);

  const resetAll = () => {
    setPopupType(null);
    setTransactionId(null);
    setQrUrl('');
    setApprovalUrl('');
    setStatus('pending');
    clearInterval(pollingRef.current);
  };

  // submit chính: định tuyến theo method
  const handleSubmit = async e => {
    e.preventDefault();
    if (!amount) return alert('Nhập số tiền!');

    if (method === 'visa') {
      setPopupType('visaForm');
    } else if (method === 'bank' || method === 'momo') {
      // tạo QR
      try {
        const { data } = await axios.post('/api/payments/create-qr', {
          method, amount
        });
        setTransactionId(data.transactionId);
        // payload do backend trả về, ví dụ "bank=ACB&account=...&amount=..."
        const payload = data.payload;
        const url = await QRCode.toDataURL(payload);
        setQrUrl(url);
        setPopupType('qr');
      } catch (err) {
        console.error(err);
        alert('Tạo QR thất bại.');
      }
    } else if (method === 'paypal') {
      try {
        const { data } = await axios.post('/api/payments/paypal', { amount });
        setApprovalUrl(data.approvalUrl);
        setPopupType('paypal');
      } catch (err) {
        console.error(err);
        alert('Khởi tạo PayPal thất bại.');
      }
    }
  };

  // khi popup QR (bank/momo) hiện, bắt đầu poll status
  useEffect(() => {
    if (popupType !== 'qr' || !transactionId) return;
    pollingRef.current = setInterval(async () => {
      try {
        const { data } = await axios.get(`/api/payments/status/${transactionId}`);
        setStatus(data.status);
        if (data.status !== 'pending') clearInterval(pollingRef.current);
      } catch (err) {
        console.error(err);
      }
    }, 3000);
    return () => clearInterval(pollingRef.current);
  }, [popupType, transactionId]);

  // xử lý submit visa
  const handleVisaPay = async e => {
    e.preventDefault();
    // validate đơn giản
    if (!cardNumber || !cardName || !expiry || !cvv) {
      return alert('Nhập đủ thông tin thẻ!');
    }
    try {
      const { data } = await axios.post('/api/payments/visa', {
        cardInfo: { cardNumber, cardName, expiry, cvv },
        amount
      });
      setTransactionId(data.transactionId);
      setPopupType('qr');   // dùng cùng popup qr để show status
      // QR ở đây ta có thể tạo payload đơn giản hoặc skip QR,
      // nhưng để dùng chung popup mình đặt 1 hình placeholder
      setQrUrl('');
    } catch (err) {
      console.error(err);
      alert('Thanh toán Visa thất bại.');
    }
  };

  return (
    <div className="paymoney-container">
      <div className="paymoney-card">
        <h1>Nạp tiền</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Số tiền:</label>
            <input
              type="number" value={amount}
              onChange={e => setAmount(e.target.value)}
              placeholder="Ví dụ: 50000"
              required
            />
          </div>
          <div className="form-group">
            <label>Phương thức:</label>
            <select
              value={method}
              onChange={e => setMethod(e.target.value)}
            >
              <option value="visa">Visa</option>
              <option value="bank">Thẻ Ngân hàng</option>
              <option value="momo">Momo</option>
              <option value="paypal">PayPal</option>
            </select>
          </div>
          <button type="submit">Tiếp tục</button>
        </form>
      </div>

      {/* --- Visa Form Popup --- */}
      {popupType === 'visaForm' && (
        <div className="qr-popup-overlay">
          <div className="qr-popup">
            <button className="close-btn" onClick={resetAll}>&times;</button>
            <h2>Nhập thông tin thẻ Visa</h2>
            <form onSubmit={handleVisaPay} className="visa-form">
              <input
                type="text"
                placeholder="Số thẻ (16 số)"
                value={cardNumber}
                onChange={e => setCardNumber(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Chủ thẻ"
                value={cardName}
                onChange={e => setCardName(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="MM/YY"
                value={expiry}
                onChange={e => setExpiry(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="CVV"
                value={cvv}
                onChange={e => setCvv(e.target.value)}
                required
              />
              <button type="submit">Thanh toán {amount}₫</button>
            </form>
          </div>
        </div>
      )}

      {/* --- QR Popup (bank, momo, visa-status) --- */}
      {popupType === 'qr' && (
        <div className="qr-popup-overlay">
          <div className="qr-popup">
            <button className="close-btn" onClick={resetAll}>&times;</button>
            <h2>Quét QR để thanh toán</h2>
            {qrUrl
              ? <img src={qrUrl} alt="QR chuyển tiền" />
              : <div className="qr-placeholder">Đang khởi tạo...</div>
            }
            <p>Số tiền: <strong>{amount}₫</strong></p>
            <p>Phương thức: <strong>{method}</strong></p>
            <p>
              Trạng thái: {' '}
              {status==='pending' && <span className="status-pending">Đang chờ</span>}
              {status==='success' && <span className="status-success">Thành công!</span>}
              {status==='failed'  && <span className="status-failed">Thất bại!</span>}
            </p>
          </div>
        </div>
      )}

      {/* --- PayPal Redirect Popup --- */}
      {popupType === 'paypal' && (
        <div className="qr-popup-overlay">
          <div className="qr-popup">
            <button className="close-btn" onClick={resetAll}>&times;</button>
            <h2>Chuyển sang PayPal</h2>
            <p>Bạn sẽ được chuyển hướng để hoàn tất thanh toán {amount}₫.</p>
            <button
              onClick={() => window.location.href = approvalUrl}
            >
              Đi tới PayPal
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PayMoney;
