import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Hàm checkLogin gọi /me
    const checkLogin = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/me", {
                method: "GET",
                credentials: "include",
            });

            // Kiểm tra response status code
            if (response.status === 401) {
                // Không log gì cả, chỉ xử lý logic
                setUser(null);
                return;
            }

            if (!response.ok) {
                // Các mã lỗi khác (404, 500, v.v.)
                console.error("Error status:", response.status);
                setUser(null);
                return;
            }

            const data = await response.json();
            // Kiểm tra data trả về
            if (data.status === "success" && data.username) {
                setUser(data.username);
            } else {
                setUser(null);
            }
        } catch (err) {
            // Ở đây tuỳ bạn, có thể không log ra console để tránh spam
            console.error("Error in checkLogin:", err);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    // Gọi một lần khi app load
    useEffect(() => {
        checkLogin();
    }, []);

    return (
        <AuthContext.Provider value={{ user, setUser, loading }}>
            {children}
        </AuthContext.Provider>
    );
};