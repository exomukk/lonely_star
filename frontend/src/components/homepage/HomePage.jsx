import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext'; // Đường dẫn đúng tới AuthContext
import './HomePage.css';

const HomePage = () => {
    const navigate = useNavigate();
    const { user } = useContext(AuthContext);

    const handleOpenCase = (caseId) => {
        if (!user) {
            alert('Bạn cần đăng nhập để mở hòm!');
            return;
        }

        if (caseId === 1) {
            navigate('/opencase/1'); // Trang mở hòm miễn phí
        } else {
            navigate(`/opencase/${caseId}`); // Trang mở hòm trả phí
        }
    };

    const caseImages = {
        1: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_community_32.png",
        2: "https://pub-5f12f7508ff04ae5925853dee0438460.r2.dev/data/csgo/resource/flash/econ/weapon_cases/crate_community_33_png.png",
        3: "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFQwnfCcJmxDv9rhwIHZwqP3a-uGwz9Xv8F0j-qQrI3xiVLkrxVuZW-mJoWLMlhpWhFkc9M",
        4: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsRVx4MwFo5_T3eAQ3i6DMIW0X7ojiwoHax6egMOKGxj4G68Nz3-jCp4itjFWx-ktqfSmtcwqVx6sT",
        5: "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fRPasw8rsUFJ5KBFZv668FFY3navMJWgQtNm1ldLZzvOiZr-BlToIsZcoi-yTpdutiVW2-Es4NWjwIo-LMlhpinMS53M"
    };

    return (
        <div className="homepage-container">
            <div className="banner">
                <img src="https://i.ytimg.com/vi/17w0L5ZQju4/maxresdefault.jpg" alt="Banner" className="banner-image" />
            </div>

            <div className="cases-grid">
                {[1, 2, 3, 4, 5].map((caseId) => (
                    <div key={caseId} className="case-item">
                        <img
                            src={caseImages[caseId]}
                            alt={`Case ${caseId}`}
                            className="case-image"
                        />
                        <button
                            className="open-case-button"
                            onClick={() => handleOpenCase(caseId)}
                        >
                            {caseId === 1 ? 'Mở Hòm Miễn Phí' : 'Mở Hòm'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomePage;