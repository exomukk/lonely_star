import React, { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './OpenCase.css';

const ITEM_WIDTH = 120;
const TARGET_INDEX = 6; // vị trí bạn muốn dừng

export default function OpenCase() {
    const { caseId } = useParams();
    const [rolling, setRolling] = useState(false);
    const [rewardItems, setRewardItems] = useState([]);
    const [displayItems, setDisplayItems] = useState([]);

    const stripRef = useRef(null);
    const containerRef = useRef(null);
    const animRef = useRef(null);

    // Load data hòm
    useEffect(() => {
        (async () => {
            try {
                const res = await fetch(
                    `${process.env.REACT_APP_API_BASE_URL}/api/chest_info/${caseId}`,
                    { credentials: 'include' }
                );
                const data = await res.json();
                if (!res.ok) {
                    alert(data.error || 'Không thể tải dữ liệu hòm!');
                    return;
                }
                const items =
                    data.type === 'cash'
                        ? data.reward_values.map(v => ({
                            name: `$${v}`,
                        }))
                        : data.skins;
                setRewardItems(items);
                setDisplayItems(items);
            } catch (err) {
                console.error(err);
                alert('Lỗi khi tải dữ liệu hòm!');
            }
        })();
    }, [caseId]);

    // Quay hòm
    const startRolling = async () => {
        if (rolling || !rewardItems.length) return;
        setRolling(true);

        // 1) Lấy kết quả
        const res = await fetch(`${process.env.REACT_APP_API_BASE_URL}/api/open_chest`, {
            method: 'POST',
            credentials: 'include',      // nếu bạn cần gửi cookie JWT
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ chest_id: caseId })
        });
        const result = await res.json();
        if (!res.ok) { alert(result.error); setRolling(false); return; }

        const wonItem = result.skin
            ? {
                name: result.skin.name,
                image: result.skin.image
            }
            : {
                name: `$${result.reward}`,
                image: `https://via.placeholder.com/${ITEM_WIDTH}x80?text=$${result.reward}`
            };

        // 2) Sắp xếp displayItems
        let others = rewardItems.filter(it => it.name !== wonItem.name);
        while (others.length < rewardItems.length - 1) others = [...others, ...others];
        const arranged = [
            ...others.slice(0, TARGET_INDEX),
            wonItem,
            ...others.slice(TARGET_INDEX)
        ].slice(0, rewardItems.length);
        setDisplayItems(arranged);

        // 3) Chuẩn bị animation
        const totalW = arranged.length * ITEM_WIDTH;
        const startPos = totalW; // bắt đầu ở bản sao giữa
        let pos = startPos;
        let vel = 30;
        const tStart = performance.now();
        const containerW = containerRef.current.clientWidth;
        const center = containerW / 2;

        // Đảm bảo tắt transition trước khi bắt đầu
        stripRef.current.style.transition = 'none';
        stripRef.current.style.transform = `translateX(${-startPos}px)`;

        // 4) Chạy frame
        const frame = now => {
            const dt = now - tStart;
            if (dt > 1500) vel *= 0.98;
            pos += vel;
            stripRef.current.style.transform = `translateX(${- (pos % (totalW * 3))}px)`;

            if (vel > 0.5) {
                animRef.current = requestAnimationFrame(frame);
            } else {
                cancelAnimationFrame(animRef.current);
                // Snap về đúng vị trí wonItem
                stripRef.current.style.transition = 'none';
                const offset = TARGET_INDEX * ITEM_WIDTH - (center - ITEM_WIDTH / 2);
                stripRef.current.style.transform = `translateX(${-(totalW + offset)
                    }px)`;
                setTimeout(() => {
                    alert(`🎉 Bạn đã nhận được: ${wonItem.name}`);
                    setRolling(false);
                }, 300);
            }
        };

        animRef.current = requestAnimationFrame(frame);
    };

    // hiển thị triple-copy
    const display = [...displayItems, ...displayItems, ...displayItems];

    return (
        <div className="open-case-container">
            <h1>Mở Hòm #{caseId}</h1>
            <div className="case-strip-container" ref={containerRef}>
                <div className="line" />
                <div className="case-strip" ref={stripRef}>
                    {display.map((item, i) => (
                        <div className="item" key={i}>
                            {<img src={item.image} alt={item.name} />}
                            <p>{item.name}</p>
                        </div>
                    ))}
                </div>
            </div>
            <button
                className="open-button"
                onClick={startRolling}
                disabled={rolling}
            >
                {rolling ? 'Đang quay...' : 'Mở Hòm'}
            </button>
        </div>
    );
}
