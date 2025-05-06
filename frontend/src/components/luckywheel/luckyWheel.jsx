import React, { useState } from 'react';
import './luckyWheel.css';

// Hardcode danh sách skin
const defaultBackpackSkins = [
    { id: 1, name: 'AK-47 | Redline', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
    { id: 2, name: 'M4A1-S | Hot Rod', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
    { id: 3, name: 'AWP | Asiimov', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
    // ... thêm tuỳ ý
];

const defaultUpgradeSkinsMap = {
    1.5: [
        { id: 4, name: 'Glock-18 | Moonrise', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
        { id: 5, name: 'P2000 | Fire Elemental', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
    ],
    2: [
        { id: 6, name: 'Desert Eagle | Blaze', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
        { id: 7, name: 'USP-S | Kill Confirmed', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
    ],
    5: [
        { id: 8, name: 'AK-47 | Vulcan', img: 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposr-kLAtl7PLZTjlH_9mkgIWKkPvxDLDEm2JS4Mp1mOjG-oLKhF2zowdyN2qhJIPHJlA_MlyGrwK9yO7njJS_uszIynRjuSNw5y6LyR211BBNZ_sv26KzzJfhhA/512fx384f' },
        // ...
    ],
    10: [ /* ... */],
    20: [ /* ... */],
    100: [ /* ... */],
};

const multiplierMap = {
    1.5: 270,
    2: 180,
    5: 75,
    10: 30,
    20: 15,
    100: 3
};

function HomePage() {
    // Vòng quay
    const [x, setX] = useState(0);
    const [y, setY] = useState(270);
    const [difference, setDifference] = useState(270);
    const [angle, setAngle] = useState(0);
    const [randomAngle, setRandomAngle] = useState(null);
    const [isSpinning, setIsSpinning] = useState(false);

    // Skin quản lý
    const [backpackSkins] = useState(defaultBackpackSkins);
    const [upgradeSkins, setUpgradeSkins] = useState(defaultUpgradeSkinsMap[1.5]);
    const [backpackSearch, setBackpackSearch] = useState('');
    const [upgradeSearch, setUpgradeSearch] = useState('');

    // Skin được chọn
    const [selectedBackpackSkin, setSelectedBackpackSkin] = useState(backpackSkins[0]);
    const [selectedUpgradeSkin, setSelectedUpgradeSkin] = useState(upgradeSkins[0]);

    // Khi chọn hệ số
    const handleSelectMultiplier = (multiplier) => {
        const diff = multiplierMap[multiplier];
        setDifference(diff);

        const list = defaultUpgradeSkinsMap[multiplier];
        setUpgradeSkins(list);
        // Reset skin nâng cấp về phần tử đầu
        setSelectedUpgradeSkin(list[0]);

        if (x + diff <= 360) setY(x + diff);
        else setY(360);
    };

    // Slider thay đổi x
    const handleSliderChange = (e) => {
        const newX = +e.target.value;
        setX(newX);
        if (newX + difference <= 360) setY(newX + difference);
        else setY(360);
    };

    // Quay
    const handleSpin = () => {
        if (isSpinning) return;
        const newRandom = Math.floor(Math.random() * 360) + 1;
        setRandomAngle(newRandom);
        setAngle((angle % 360) + 1080 + newRandom);
        setIsSpinning(true);
    };

    const handleTransitionEnd = () => {
        if (!isSpinning) return;
        setIsSpinning(false);
        if (randomAngle !== null) {
            if (randomAngle >= x && randomAngle <= y) {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THẮNG!`);
            } else {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THUA!`);
            }
            window.location.reload();
        }
    };

    // Filter
    const filteredBackpack = backpackSkins.filter(s =>
        s.name.toLowerCase().includes(backpackSearch.toLowerCase())
    );
    const filteredUpgrade = upgradeSkins.filter(s =>
        s.name.toLowerCase().includes(upgradeSearch.toLowerCase())
    );

    return (
        <div className="homepage-container">
            <h2>Game Vòng Quay May Mắn</h2>

            {/* Chọn multiplier */}
            <div className="multiplier-buttons">
                {Object.keys(multiplierMap).map(m => (
                    <button
                        key={m}
                        onClick={() => handleSelectMultiplier(Number(m))}
                    >
                        x{m}
                    </button>
                ))}
            </div>

            {/* Slider */}
            <div className="slider-container">
                <label>Chọn khoảng bắt đầu:</label>
                <input
                    type="range"
                    min="0"
                    max={360 - difference}
                    value={x}
                    onChange={handleSliderChange}
                />
            </div>

            {/* Hai ô skin nhỏ */}
            <div className="side-skins">
                <div className="side-box left">
                    <img src={selectedBackpackSkin?.img} alt="" />
                    <p>{selectedBackpackSkin?.name}</p>
                </div>
                <div className="side-box right">
                    <img src={selectedUpgradeSkin?.img} alt="" />
                    <p>{selectedUpgradeSkin?.name}</p>
                </div>
            </div>

            {/* Vòng quay */}
            <div className="wheel-container">
                <div
                    className="wheel"
                    style={{ '--start': `${x}deg`, '--end': `${y}deg` }}
                />
                <div
                    className="pointer"
                    style={{ transform: `translate(-50%, -80px) rotate(${angle}deg)` }}
                    onTransitionEnd={handleTransitionEnd}
                />
            </div>
            <button onClick={handleSpin}>Quay</button>

            {/* Hai ô lớn với search */}
            <div className="skins-container">
                <div className="large-box">
                    <h4>Skin trong balo</h4>
                    <input
                        className="search-input"
                        type="text"
                        placeholder="Tìm kiếm skin..."
                        value={backpackSearch}
                        onChange={e => setBackpackSearch(e.target.value)}
                    />
                    <div className="skin-list">
                        {filteredBackpack.map(skin => (
                            <div
                                key={skin.id}
                                className="skin-item"
                                onClick={() => setSelectedBackpackSkin(skin)}
                                style={{
                                    border: skin.id === selectedBackpackSkin.id
                                        ? '2px solid red' : '1px solid #333'
                                }}
                            >
                                <img src={skin.img} alt="" />
                                <p>{skin.name}</p>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="large-box">
                    <h4>Skin có thể nâng cấp</h4>
                    <input
                        className="search-input"
                        type="text"
                        placeholder="Tìm kiếm skin..."
                        value={upgradeSearch}
                        onChange={e => setUpgradeSearch(e.target.value)}
                    />
                    <div className="skin-list">
                        {filteredUpgrade.map(skin => (
                            <div
                                key={skin.id}
                                className="skin-item"
                                onClick={() => setSelectedUpgradeSkin(skin)}
                                style={{
                                    border: skin.id === selectedUpgradeSkin.id
                                        ? '2px solid red' : '1px solid #333'
                                }}
                            >
                                <img src={skin.img} alt="" />
                                <p>{skin.name}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
