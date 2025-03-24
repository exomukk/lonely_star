// src/components/user/UserProfile.jsx
import React, { useState } from 'react';

const UserProfile = () => {
    // Giả lập dữ liệu người dùng
    const [name, setName] = useState('béo');
    const [email, setEmail] = useState('beo@example.com');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Logic update (gọi API v.v.)
        console.log('Thông tin mới:', { name, email });
        alert('Cập nhật thông tin thành công (demo)');
    };

    return (
        <div style={{ padding: '1rem' }}>
            <h1>Thông tin người dùng</h1>
            <form onSubmit={handleSubmit} style={{ maxWidth: '400px' }}>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Tên: </label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        style={{ width: '100%' }}
                    />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Email: </label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{ width: '100%' }}
                    />
                </div>
                <button type="submit">Cập nhật</button>
            </form>
        </div>
    );
};

export default UserProfile;
