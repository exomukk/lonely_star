import React, { useState, useEffect } from 'react';
import './luckyWheel.css';

const MULTIPLIERS = [1.5, 2, 5, 10, 20, 100];
const API = process.env.REACT_APP_API_BASE_URL;

export default function HomePage() {
    const [backpackSearch, setBackpackSearch] = useState('');
    const [upgradeSearch, setUpgradeSearch] = useState('');
    // —— Inventory từ backend
    const [items, setItems] = useState([]);
    const [selectedBackpackSkin, setSelectedBackpackSkin] = useState(null);

    // —— Upgrade options
    const [upgradeSkins, setUpgradeSkins] = useState([]);
    const [selectedUpgradeSkin, setSelectedUpgradeSkin] = useState(null);

    // —— Wheel state
    const [x, setX] = useState(0);         // start angle
    const [difference, setDifference] = useState(270); // sweep angle
    const [y, setY] = useState(270);       // end angle = x + difference
    const [angle, setAngle] = useState(0);
    const [randomAngle, setRandomAngle] = useState(null);
    const [isSpinning, setIsSpinning] = useState(false);

    // roll rate
    const [rate, setRate] = useState(null);

    // gọi API rollRate và lưu kết quả vào state hoặc log ra console
    const rollRateApi = async (upSkin) => {
        if (!selectedBackpackSkin) {
            alert('Hãy chọn trước skin trong balo!');
            return;
        }
        const params = new URLSearchParams({
            userWeaponID: selectedBackpackSkin.skin_id,
            expectedWeaponID: upSkin.id,
        });
        try {
            const res = await fetch(`${API}/api/rollRate?${params}`, {
                method: 'GET',
                credentials: 'include',
            });
            const data = await res.json();
            if (res.ok) {
                console.log('Tỉ lệ thành công:', data.rate);
                setRate(data.rate);  // nếu bạn muốn hiển thị hoặc dùng tiếp
            } else {
                alert(data.error || 'Không lấy được tỉ lệ');
            }
        } catch (err) {
            console.error(err);
            alert('Lỗi khi gọi rollRate');
        }
    };

    // 1) Load inventory + skin_info
    useEffect(() => {
        fetch(`${API}/api/inventory`, { credentials: 'include' })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    Promise.all(
                        data.inventory.map(item =>
                            fetch(`${API}/api/skin/${item.skin_id}`, { credentials: 'include' })
                                .then(r => r.json())
                                .then(skin => ({
                                    skin_id: item.skin_id,
                                    quantity: item.quantity,
                                    skin_info: skin
                                }))
                        )
                    ).then(full => setItems(full));
                }
            })
            .catch(console.error);
    }, []);

    // 2) Chọn multiplier → fetch upgradeSkins theo price_range
    const handleSelectMultiplier = async m => {
        if (!selectedBackpackSkin) {
            alert('Hãy chọn 1 skin trong balo trước!');
            return;
        }
        const price = selectedBackpackSkin.skin_info.price;

        try {
            const res = await fetch(`${API}/api/gun/price_range`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    base_price: price,
                    multiplier: m
                })
            });
            const data = await res.json();
            if (res.ok && data.status === 'success') {
                setUpgradeSkins(data.guns);
                setSelectedUpgradeSkin(data.guns[0] || null);
            } else {
                alert(data.message || 'Không lấy được danh sách nâng cấp');
            }
        } catch (err) {
            console.error(err);
            alert('Lỗi khi gọi price_range');
        }
    };

    // 3) Slider (nếu bạn cần cho wheel preview vùng thắng)
    const handleSliderChange = e => {
        const v = +e.target.value;
        setX(v);
        setY(v + difference <= 360 ? v + difference : 360);
    };

    // 4) Quay → gọi rollRate → animate
    const handleSpin = async () => {
        if (isSpinning) return;
        if (!selectedBackpackSkin || !selectedUpgradeSkin) {
            alert('Chọn cả 2 skin trước khi quay!');
            return;
        }

        try {
            // 1) Lấy rate để vẽ vùng đỏ
            const rateRes = await fetch(`${API}/api/rollRate?` + new URLSearchParams({
                userWeaponID: selectedBackpackSkin.skin_id,
                expectedWeaponID: selectedUpgradeSkin.id
            }), { credentials: 'include' });
            const rateData = await rateRes.json();
            if (!rateRes.ok) {
                alert(rateData.error || 'Lỗi rollRate');
                return;
            }
            const sweep = rateData.rate * 3.6;
            setDifference(sweep);
            setY(x + sweep <= 360 ? x + sweep : 360);

            // 2) Gọi upgradeSkin để biết win hay lose
            const upgradeRes = await fetch(`${API}/api/upgradeSkin`, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userWeaponID: selectedBackpackSkin.skin_id,
                    expectedWeaponID: selectedUpgradeSkin.id,
                    startRange: x,
                    endRange: x + sweep  // hoặc y
                })
            });
            const { success } = await upgradeRes.json();
            // success === true ⇒ thắng, ngược lại ⇒ thua

            // 3) Tính góc dừng cố định
            let fixedAngle;
            if (success) {
                // giữa vùng thắng (x → x+sweep)
                fixedAngle = Math.round(x + sweep / 2) % 360;
            } else {
                // giữa vùng thua (x+sweep → x+360)
                const losingStart = (x + sweep) % 360;
                const losingSweep = 360 - sweep;
                fixedAngle = Math.round(losingStart + losingSweep / 2) % 360;
            }
            setRandomAngle(fixedAngle);

            // 4) Bắt đầu animation: +1080 độ để kim quay đủ lâu
            setAngle(prev => (prev % 360) + 1080 + fixedAngle);
            setIsSpinning(true);

        } catch (err) {
            console.error(err);
            alert('Lỗi khi quay');
        }
    };
    const handleTransitionEnd = () => {
        setIsSpinning(false);
        if (randomAngle !== null) {
            const win = randomAngle >= x && randomAngle <= y;
            alert(`Bạn đã ${win ? 'THẮNG' : 'THUA'}!`);
            window.location.reload();
        }
    };

    // 5) Filter
    const filteredBackpack = items.filter(item =>
        item.skin_info.name.toLowerCase().includes(backpackSearch.toLowerCase())
    );
    const filteredUpgrade = upgradeSkins.filter(skin =>
        skin.name.toLowerCase().includes(upgradeSearch.toLowerCase())
    );

    return (
        <div className="homepage-container">
            <h2>Game Vòng Quay May Mắn</h2>

            {/* Chọn multiplier */}
            <div className="multiplier-buttons">
                {MULTIPLIERS.map(m => (
                    <button key={m} onClick={() => handleSelectMultiplier(m)}>
                        x{m}
                    </button>
                ))}
            </div>

            {/* Slider preview vùng thắng */}
            <div className="slider-container">
                <label>Chọn khoảng bắt đầu:</label>
                <input
                    type="range"
                    min="0" max={360 - difference}
                    value={x} onChange={handleSliderChange}
                />
            </div>

            {/* Ô preview */}
            <div className="side-skins">
                <div className="side-box left">
                    {selectedBackpackSkin ? (
                        <>
                            <img
                                src={selectedBackpackSkin.skin_info.image}
                                alt={selectedBackpackSkin.skin_info.name}
                            />
                            <p>{selectedBackpackSkin.skin_info.name}</p>
                        </>
                    ) : (
                        <div className="empty-box" />
                    )}
                </div>
                <div className="side-box right">
                    {selectedUpgradeSkin ? (
                        <>
                            <img
                                src={selectedUpgradeSkin.image}
                                alt={selectedUpgradeSkin.name}
                            />
                            <p>{selectedUpgradeSkin.name}</p>
                        </>
                    ) : (
                        <div className="empty-box" />
                    )}
                </div>
            </div>

            {/* Wheel */}
            <div className="wheel-container">
                <div
                    className="wheel"
                    style={{ '--start': `${rate !== null ? 0 : x}deg`, '--end': `${rate !== null ? (rate * 3.6).toFixed(2) : y}deg` }}
                />
                <div
                    className="pointer"
                    style={{ transform: `translate(-50%, -80px) rotate(${angle}deg)` }}
                    onTransitionEnd={handleTransitionEnd}
                />
            </div>
            <button onClick={handleSpin} disabled={isSpinning}>
                {isSpinning ? 'Đang quay...' : 'Quay'}
            </button>

            {rate !== null && <p>Tỉ lệ thành công: {Math.round(rate)}%</p>}

            {/* Skin trong balo */}
            <div className="skins-container">
                <div className="large-box">
                    <h4>Skin trong balo</h4>
                    <input
                        className="search-input"
                        placeholder="Tìm kiếm skin..."
                        value={backpackSearch}
                        onChange={e => setBackpackSearch(e.target.value)}
                    />
                    <div className="skin-list">
                        {filteredBackpack.map(item => (
                            <div
                                key={item.skin_id}
                                className="skin-item"
                                onClick={() => setSelectedBackpackSkin(item)}
                                style={{
                                    border: item.skin_id === selectedBackpackSkin?.skin_id
                                        ? '2px solid red'
                                        : '1px solid #333'
                                }}
                            >
                                <img
                                    src={item.skin_info.image}
                                    alt={item.skin_info.name}
                                />
                                <p>{item.skin_info.name}</p>
                                <small>Số lượng: {item.quantity}</small>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Skin nâng cấp */}
                <div className="large-box">
                    <h4>Skin có thể nâng cấp</h4>
                    <input
                        className="search-input"
                        placeholder="Tìm kiếm skin..."
                        value={upgradeSearch}
                        onChange={e => setUpgradeSearch(e.target.value)}
                    />
                    <div className="skin-list">
                        {filteredUpgrade.map(skin => (
                            <div
                                key={skin.id}
                                className="skin-item"
                                onClick={() => {
                                    setSelectedUpgradeSkin(skin);
                                    rollRateApi(skin);
                                }}
                                style={{
                                    border: skin.id === selectedUpgradeSkin?.id
                                        ? '2px solid red'
                                        : '1px solid #333'
                                }}
                            >
                                <img src={skin.image} alt={skin.name} />
                                <p>{skin.name}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
