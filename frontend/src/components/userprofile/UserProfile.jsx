import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

const UserProfile = () => {
    // Giả lập dữ liệu người dùng
    const [name, setName] = useState('béo');
    const [email, setEmail] = useState('beo@example.com');
    const [items, setItems] = useState([]);      // dữ liệu kho đồ
    const navigate = useNavigate();

    // useEffect để giả lập fetch từ server
    useEffect(() => {
        // TODO: thay bằng fetch('/api/my-skins').then(res => res.json())...
        const mockedItems = [
            {
                name: "AUG | Anodized Navy",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot6-iFAZu7P3JZyR97s63go-0m_7zO6-fz24Bu5Iji-rFodmm3Qzjr0o-Nz_xddLEdVU7ZA7Q_1W_xbu51JDptYOJlyWB_uSARA/512fx384f"
            },
            {
                name: "AUG | Ricochet",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot6-iFAZt7PLddgJI-dG0mIW0m_7zO6-fkjpX65Um2evA9tX2jQDl80I4ZjqmIYKVJAFoMArV_VjtwL290JK8uoOJlyUdLwiicA/512fx384f"
            },
            {
                name: "AWP | PAW",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAZt7PLfYQJS7cumlZe0m_7zO6-fx2oH7JYkiO-Z9or3jAbtr0VkZmz0IIOdcANsM1jT81a-yefqgZC1v4OJlyUJgMft6w/512fx384f"
            },
            {
                name: "CZ75-Auto | Jungle Dashed",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotaDyfgZfwOP3ZTxS6eOlnI-Zg8j-JrXWmm5u5Mx2gv2PoNyn2g3lqhFuYW_3d4-WcAE-MAvZ-QK5lLjog8C66smbznU1siVw7GGdwUJAMFqeHA/512fx384f"
            },
            {
                name: "Desert Eagle | Kumicho Dragon",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f"
            },
            {
                name: "AUG | Anodized Navy",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot6-iFAZu7P3JZyR97s63go-0m_7zO6-fz24Bu5Iji-rFodmm3Qzjr0o-Nz_xddLEdVU7ZA7Q_1W_xbu51JDptYOJlyWB_uSARA/512fx384f"
            },
            {
                name: "AUG | Ricochet",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot6-iFAZt7PLddgJI-dG0mIW0m_7zO6-fkjpX65Um2evA9tX2jQDl80I4ZjqmIYKVJAFoMArV_VjtwL290JK8uoOJlyUdLwiicA/512fx384f"
            },
            {
                name: "AWP | PAW",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAZt7PLfYQJS7cumlZe0m_7zO6-fx2oH7JYkiO-Z9or3jAbtr0VkZmz0IIOdcANsM1jT81a-yefqgZC1v4OJlyUJgMft6w/512fx384f"
            },
            {
                name: "CZ75-Auto | Jungle Dashed",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotaDyfgZfwOP3ZTxS6eOlnI-Zg8j-JrXWmm5u5Mx2gv2PoNyn2g3lqhFuYW_3d4-WcAE-MAvZ-QK5lLjog8C66smbznU1siVw7GGdwUJAMFqeHA/512fx384f"
            },
            {
                name: "Desert Eagle | Kumicho Dragon",
                image: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f"
            }
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
                    {items.map(item => (
                        <div key={item.id} className="inventory-item">
                            <img src={item.image} alt={item.name} />
                            <p>{item.name}</p>
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