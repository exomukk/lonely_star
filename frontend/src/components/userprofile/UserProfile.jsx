import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

const API = process.env.REACT_APP_API_BASE_URL;

const UserProfile = () => {
    // User info
    const [name, setName] = useState('béo');
    const [email, setEmail] = useState('beo@example.com');

    // Inventory and cash
    const [items, setItems] = useState([]);
    const [cash, setCash] = useState(0);

    // Admin flag and server status
    const [isAdmin, setIsAdmin] = useState(false);
    const [serverStatus, setServerStatus] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        // Lấy kho đồ
        fetch(`${API}/api/inventory`, { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    return Promise.all(
                        data.inventory.map(item =>
                            fetch(`${API}/api/skin/${item.skin_id}`, { credentials: 'include' })
                                .then(res => res.json())
                                .then(skin => ({ ...item, skin_info: skin }))
                        )
                    );
                }
                throw new Error('Lỗi lấy inventory');
            })
            .then(setItems)
            .catch(err => console.error('Inventory fetch error:', err));

        // Lấy số dư
        fetch(`${API}/api/currentCash`, { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                if (data.cash !== undefined) setCash(data.cash);
                else console.warn('Không có cash:', data);
            })
            .catch(err => console.error('Cash fetch error:', err));

        // Kiểm tra quyền admin
        fetch(`${API}/api/is_admin`, { credentials: 'include' })
            .then(res => res.json())
            .then(data => setIsAdmin(data.admin === 'true'))
            .catch(err => console.error('Admin check error:', err));
    }, []);

    const handleSubmit = e => {
        e.preventDefault();
        alert('Cập nhật thông tin thành công (demo)');
    };

    const handleSell = skinId => {
        fetch(`${API}/api/sell_skin`, {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ skin_id: skinId })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('Đã bán thành công!');
                    window.location.reload();
                } else {
                    alert('Lỗi khi bán súng: ' + data.message);
                }
            })
            .catch(err => console.error('Sell error:', err));
    };

    const handleFund = e => {
        e.preventDefault();
        navigate('/paymoney');
    };

    const handleCheckServer = () => {
        fetch(`${API}/api/check`, { credentials: 'include' })
            .then(res =>
                res.json().then(body => ({ status: res.status, body }))
            )
            .then(({ status, body }) => {
                if (status === 200) {
                    const { status: st, message, 'CPU Usage': cpu, 'Memory Usage': mem } = body;
                    alert(
                        `Status: ${st}\n` +
                        `Message: ${message}\n` +
                        `CPU Usage: ${cpu}%\n` +
                        `Memory Usage: ${mem.ram_usage_percent}%`
                    );
                } else {
                    alert(body.error || 'Không có quyền truy cập');
                }
            })
            .catch(err => console.error('Check server error:', err));
    };


    return (
        <div className="profile-container">
            <div className="profile-card">
                <h1>Thông tin người dùng</h1>
                <h3>Số dư hiện tại: {(Math.ceil(cash * 100) / 100).toFixed(2)}</h3>

                <form onSubmit={handleSubmit} className="profile-form">
                    <div>
                        <label>Tên: </label>
                        <input
                            type="text"
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                    </div>
                    <div>
                        <label>Email: </label>
                        <input
                            type="email"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                    </div>
                    <button type="submit">Cập nhật</button>
                </form>

                <button onClick={handleFund} className="profile-fund-button">
                    Nạp tiền
                </button>

                {isAdmin && (
                    <>
                        <button onClick={handleCheckServer} className="profile-check-button">
                            Kiểm tra server
                        </button>
                        {serverStatus && (
                            <div className="server-status">
                                <p>Status: {serverStatus.status}</p>
                                <p>Message: {serverStatus.message}</p>
                                <p>CPU Usage: {serverStatus['CPU Usage']}%</p>
                                <p>Memory Usage: {serverStatus['Memory Usage']}%</p>
                            </div>
                        )}
                    </>
                )}
            </div>

            <h2 className="inventory-title">Kho đồ của bạn</h2>
            <div className="inventory-grid">
                {items.length > 0 ? (
                    items.map(item => (
                        <div key={item.skin_id} className="inventory-item-card">
                            <img
                                src={item.skin_info?.image}
                                alt={item.skin_info?.name}
                                className="skin-image"
                            />
                            <div className="skin-info">
                                <h4>{item.skin_info?.name}</h4>
                                <p>
                                    Độ hiếm: <strong>{item.skin_info?.tierlist}</strong>
                                </p>
                                <p>Giá: ${item.skin_info?.price}</p>
                                <p>Số lượng: {item.quantity || 1}</p>
                                <button
                                    className="sell-button"
                                    onClick={() => handleSell(item.skin_id)}
                                >
                                    Bán súng
                                </button>
                            </div>
                        </div>
                    ))
                ) : (
                    <p>Chưa có skin nào trong kho đồ.</p>
                )}
            </div>
        </div>
    );
};

export default UserProfile;