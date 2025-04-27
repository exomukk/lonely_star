import React, { useState } from 'react';
import './luckyWheel.css';

// Map hệ số -> độ rộng "khoảng trúng" (y - x)
const multiplierMap = {
    1.5: 270,
    2: 180,
    5: 75,
    10: 30,
    20: 15,
    100: 3
};

function HomePage() {
    // X là góc bắt đầu, Y là góc kết thúc
    const [x, setX] = useState(0);
    const [y, setY] = useState(270);  // mặc định x1.5 => 270°
    // Lưu “độ rộng” của khoảng trúng (mặc định 270° tương ứng x1.5)
    const [difference, setDifference] = useState(270);

    const [angle, setAngle] = useState(0);     // Góc hiện tại của kim
    const [randomAngle, setRandomAngle] = useState(null);
    const [isSpinning, setIsSpinning] = useState(false);

    // Chọn hệ số: gán difference và tính lại y
    const handleSelectMultiplier = (multiplier) => {
        const diff = multiplierMap[multiplier];
        setDifference(diff);

        // Nếu x + diff <= 360 thì y = x + diff
        // Ngược lại, clamp y = 360 (để đơn giản, không wrap-around)
        if (x + diff <= 360) {
            setY(x + diff);
        } else {
            setY(360);
        }
    };

    // Thanh kéo thay đổi góc bắt đầu x
    const handleSliderChange = (e) => {
        const newX = parseInt(e.target.value, 10);
        setX(newX);

        // Tính y = x + difference, nếu > 360 thì clamp = 360
        if (newX + difference <= 360) {
            setY(newX + difference);
        } else {
            setY(360);
        }
    };

    const handleSpin = () => {
        if (isSpinning) return;

        // Tạo góc ngẫu nhiên 1-360
        const newRandomAngle = Math.floor(Math.random() * 360) + 1;
        setRandomAngle(newRandomAngle);

        // Tính góc quay cuối = góc hiện tại + 3 vòng (1080°) + randomAngle
        const finalAngle = (angle % 360) + 1080 + newRandomAngle;

        // Bắt đầu quay
        setAngle(finalAngle);
        setIsSpinning(true);
    };

    // Xử lý khi quay xong (transition end)
    const handleTransitionEnd = () => {
        if (!isSpinning) return;
        setIsSpinning(false);

        if (randomAngle !== null) {
            // randomAngle nằm trong khoảng [x, y] => thắng
            if (randomAngle >= x && randomAngle <= y) {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THẮNG!`);
                window.location.reload();
            } else {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THUA!`);
                window.location.reload();
            }
        }
    };

    return (
        <div className="homepage-container">
            <h2>Game Vòng Quay May Mắn</h2>

            {/* Chọn hệ số (x1.5, x2, x5, x10, x20, x100) */}
            <div className="multiplier-buttons">
                <button onClick={() => handleSelectMultiplier(1.5)}>x1.5</button>
                <button onClick={() => handleSelectMultiplier(2)}>x2</button>
                <button onClick={() => handleSelectMultiplier(5)}>x5</button>
                <button onClick={() => handleSelectMultiplier(10)}>x10</button>
                <button onClick={() => handleSelectMultiplier(20)}>x20</button>
                <button onClick={() => handleSelectMultiplier(100)}>x100</button>
            </div>

            {/* Thanh kéo chọn góc bắt đầu x (0 -> 360 - difference) */}
            <div className="slider-container">
                <label>Chọn khoảng bắt đầu:</label>
                <input
                    type="range"
                    min="0"
                    max={360 - difference}
                    value={x}
                    onChange={handleSliderChange}
                />
                {/* Xóa dòng "Khoảng trúng" như yêu cầu */}
            </div>

            {/* Vùng hiển thị vòng quay */}
            <div className="wheel-container">
                {/* Vòng tròn: dùng conic-gradient để đánh dấu khoảng [x, y] */}
                <div
                    className="wheel"
                    style={{
                        '--start': `${x}deg`,
                        '--end': `${y}deg`
                    }}
                />
                <div
                    className="pointer"
                    style={{ transform: `translateX(-50%) rotate(${angle}deg)` }}
                    onTransitionEnd={handleTransitionEnd}
                />
            </div>

            <button onClick={handleSpin}>Quay</button>
        </div>
    );
}

export default HomePage;
