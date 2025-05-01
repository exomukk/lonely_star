import React, { useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import './OpenCase.css';

// Đây là list skin (mình fix cứng 10 skin từ JSON của bạn)
const skins = [
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

const ITEM_WIDTH = 120; // px

// Fisher–Yates shuffle
function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

export default function OpenCase() {
    const { caseId } = useParams();
    const [rolling, setRolling] = useState(false);
    const stripRef = useRef(null);
    const containerRef = useRef(null);
    const animRef = useRef(null);

    // Đây là mảng sẽ shuffle mỗi lượt
    const [order, setOrder] = useState(skins);

    const startRolling = () => {
        if (rolling) return;
        setRolling(true);

        // 1) Shuffle mảng
        const newOrder = shuffle([...skins]);
        setOrder(newOrder);

        // 2) triple-copy để đủ đồ bên trái / phải
        const totalWidth = newOrder.length * ITEM_WIDTH;
        let position = totalWidth;    // bắt đầu tại offset = 1 copy
        let velocity = 30;            // px/frame
        const t0 = performance.now();

        const containerW = containerRef.current.clientWidth;
        const centerPos = containerW / 2;

        const frame = now => {
            const elapsed = now - t0;
            // 1.5s đầu chạy nhanh
            if (elapsed > 1500) velocity *= 0.98;
            position += velocity;

            // map triple-array
            stripRef.current.style.transform =
                `translateX(${- (position % (totalWidth * 3))}px)`;

            if (velocity > 0.5) {
                animRef.current = requestAnimationFrame(frame);
            } else {
                cancelAnimationFrame(animRef.current);

                // Tính index real trong newOrder:
                let rawIndex = (position + centerPos - ITEM_WIDTH / 2) / ITEM_WIDTH;
                let index = Math.round(rawIndex) % newOrder.length;
                if (index < 0) index += newOrder.length;

                // Căn strip chính xác:
                const finalOffset = index * ITEM_WIDTH - (centerPos - ITEM_WIDTH / 2);
                // bắt đầu lại từ copy đầu tiên:
                stripRef.current.style.transform =
                    `translateX(${- (totalWidth + finalOffset)}px)`;

                setTimeout(() => {
                    alert(`🎉 Bạn đã nhận được skin: ${newOrder[index].name}`);
                    setRolling(false);
                }, 300);
            }
        };

        animRef.current = requestAnimationFrame(frame);
    };

    // Dãy hiển thị = 3 lần order
    const display = [...order, ...order, ...order];

    return (
        <div className="open-case-container">
            <h1>Mở Hòm #{caseId}</h1>

            <div className="case-strip-container" ref={containerRef}>
                <div className="line" />
                <div className="case-strip" ref={stripRef}>
                    {display.map((skin, i) => (
                        <div className="item" key={i}>
                            <img src={skin.image} alt={skin.name} />
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