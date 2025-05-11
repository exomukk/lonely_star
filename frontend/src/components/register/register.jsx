import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import OTPModal from '../otp/OTP';
import './register.css';

const Register = () => {
  const [formData, setFormData] = useState({ name: '', username: '', password: '' });
  const [errorMessage, setError] = useState('');
  const [successMessage, setSuccess] = useState('');
  const [showOtpModal, setShowOtpModal] = useState(false);

 
  const [registeredEmail, setRegisteredEmail] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setSuccess('');

    console.log(`Register: ${process.env.REACT_APP_API_BASE_URL}/register`)
    try {
      const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();

      if (res.ok) {
        setSuccess('Đăng ký thành công! Vui lòng nhập mã OTP để kích hoạt.');
        setRegisteredEmail(formData.username);
        // Mở popup OTP
        setShowOtpModal(true);
      } else {
        setError(data.message || 'Đăng ký thất bại. Vui lòng thử lại.');
      }
    } catch (err) {
      setError('Lỗi mạng. Vui lòng thử lại.');
    }
  };

  const handleOtpSuccess = () => {
    // Nếu xác thực OTP thành công thì chuyển về trang chủ
    window.location.href = '/login';
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
        <input
          type="email"
          name="username"
          placeholder="Email"
          value={formData.username}
          onChange={handleInputChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
        <button type="submit">Register</button>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>

      {showOtpModal && (
        <OTPModal
          email={registeredEmail}
          onVerifySuccess={handleOtpSuccess}
          onClose={() => setShowOtpModal(false)}
        />
      )}
    </div>
  );
};

export default Register;