import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

const UserProfile = () => {
    // Giả lập dữ liệu người dùng
    const [name, setName] = useState('béo');
    const [email, setEmail] = useState('beo@example.com');
    const [items, setItems] = useState([]);      // dữ liệu kho đồ
    const navigate = useNavigate();
    const [cash, setCash] = useState(0); //so du tai khoan

    // useEffect để giả lập fetch từ server
    useEffect(() => {
        // ✅ ADDED: Gọi API thật để lấy kho đồ
        fetch("https://localhost:5000/api/inventory", {
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                setItems(data.inventory);
            }
        });

        // ✅ ADDED: Gọi API để lấy số dư
        fetch("https://localhost:5000/api/currentCash", {
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            if (data.cash !== undefined) setCash(data.cash);
        });

        // TODO: thay bằng fetch('/api/my-skins').then(res => res.json())...
        const mockedItems = [

        ];
        setItems(mockedItems);
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
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
                {/* ✅ ADDED: Hiển thị số dư */}
                <h3>Số dư hiện tại: ${cash}</h3>

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
            {/* Phần Inventory */}
            <h2 className="inventory-title">Kho đồ của bạn</h2>
                <div className="inventory-grid">
                    {/* ✅ ADDED: map theo dữ liệu thật */}
                    {items.map(item => (
                        <div key={item.skin_id} className="inventory-item">
                            <p>Skin ID: {item.skin_id}</p>
                            <p>Số lượng: {item.quantity || 1}</p>
                        </div>
                    ))}
                    {items.length === 0 && (
                        <p>Chưa có skin nào trong kho đồ.</p>
                    )}
                </div>
        </div>
    );
};

export default UserProfile;
