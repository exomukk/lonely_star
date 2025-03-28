// src/components/user/UserProfile.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

const UserProfile = () => {
    // Giả lập dữ liệu người dùng
    const [name, setName] = useState('béo');
    const [email, setEmail] = useState('beo@example.com');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Logic update (gọi API v.v.)
        console.log('Thông tin mới:', { name, email });
        alert('Cập nhật thông tin thành công (demo)');
    };

    const fund = (e) => {
        e.preventDefault();
        navigate('/paymoney');
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                <h1>Thông tin người dùng</h1>
                <form onSubmit={handleSubmit} className="profile-form">
                    <div>
                        <label>Tên: </label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>
                    <div>
                        <label>Email: </label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>
                    <button type="submit">Cập nhật</button>
                </form>
                <button onClick={fund} className="profile-fund-button">Nạp tiền</button>
            </div>
        </div>
    );
};

export default UserProfile;
