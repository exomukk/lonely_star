import React, { useState } from 'react';
import './main.css';

function HomePage() {
    const [x, setX] = useState('0');           // Giá trị góc bắt đầu (string)
    const [y, setY] = useState('0');           // Giá trị góc kết thúc (string)
    const [angle, setAngle] = useState(0);     // Góc hiện tại của kim
    const [randomAngle, setRandomAngle] = useState(null);
    const [isSpinning, setIsSpinning] = useState(false); // đánh dấu đang quay

    const handleSpin = () => {
        if (isSpinning) return;  // Nếu đang quay thì không cho quay tiếp

        // Ép x, y sang số
        const xNum = parseInt(x, 10);
        const yNum = parseInt(y, 10);

        if (xNum > yNum) {
            alert('Vui lòng nhập X < Y để xác định khoảng độ chính xác!');
            return;
        }

        // Tạo góc ngẫu nhiên 1-360
        const newRandomAngle = Math.floor(Math.random() * 360) + 1;
        setRandomAngle(newRandomAngle);

        // Tính góc quay cuối cùng = góc hiện tại + 3 vòng (1080°) + randomAngle
        // Bạn có thể dùng angle % 360 để tránh giá trị quá lớn
        const finalAngle = (angle % 360) + 1080 + newRandomAngle;

        // Bắt đầu quay
        setAngle(finalAngle);
        setIsSpinning(true);
    };

    // Hàm xử lý khi quay xong (transition kết thúc)
    const handleTransitionEnd = () => {
        if (!isSpinning) return;  // Chỉ xử lý nếu vừa quay

        setIsSpinning(false);

        // Ép x, y sang số để kiểm tra
        const xNum = parseInt(x, 10);
        const yNum = parseInt(y, 10);

        // Kiểm tra kết quả
        if (randomAngle !== null) {
            if (randomAngle >= xNum && randomAngle <= yNum) {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THẮNG!`);
            } else {
                alert(`Góc ra là ${randomAngle}° - Bạn đã THUA!`);
            }
        }
    };

    return (
        <div className="homepage-container">
            <h2>Game Vòng Quay May Mắn</h2>

            {/* Khu vực nhập khoảng x-y */}
            <div className="input-container">
                <label>
                    X (độ bắt đầu):
                    <input
                        type="number"
                        value={x}
                        onChange={(e) => setX(e.target.value)}
                    />
                </label>
                <label>
                    Y (độ kết thúc):
                    <input
                        type="number"
                        value={y}
                        onChange={(e) => setY(e.target.value)}
                    />
                </label>
            </div>

            {/* Vùng hiển thị vòng tròn + kim */}
            <div className="wheel-container">
                {/* Vòng tròn tĩnh, không quay */}
                <div className="wheel" />

                {/* Kim - quay 3 vòng + randomAngle, chờ kết thúc mới alert */}
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
