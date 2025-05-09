import React, { useEffect, useState } from 'react';
import './NavBar.css';

const Navbar = () => {
  const [user, setUser] = useState(null); // Ban đầu chưa có user
  const [showDropdown, setShowDropdown] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/me`, {
          method: 'GET',
          credentials: 'include',  // Gửi cookie kèm theo request
        });

        if (response.status === 401) {
          // 401 => token không hợp lệ, set user = null, KHÔNG log gì thêm
          setUser(null);
          return;
        }

        if (!response.ok) {
          // Các mã lỗi khác (404, 500...) => tuỳ bạn muốn xử lý hay log
          console.error('Error status:', response.status);
          setUser(null);
          return;
        }

        // Chuyển response thành JSON và log kết quả
        const data = await response.json();

        if (data.status === 'success' && data.username) {
          setUser(data.username);
          console.log(data.username)
        } else {
          setUser(null);
        }
      } catch (error) {
        setUser(null);
      }
    };

    fetchUser();
  }, []);

  const handleUserClick = () => {
    setShowDropdown(!showDropdown);
  };

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  const handleLogout = async () => {
    const csrfToken = getCookie('csrf_access_token'); // Lấy CSRF token từ cookie
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/logout`, {
        method: 'POST',
        credentials: 'include',  // Gửi cookie kèm theo request
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': csrfToken, // Gửi CSRF token trong header
        },
      });
      const result = await response.json();
      console.log('Logout response:', result);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Sau khi logout (dù có lỗi hay không), xoá thông tin user ở client
      setUser(null);
      setShowDropdown(false);
      // window.location.href = '/';
    }
  };

  return (
    <div className="navbar">
      {/* Icon hamburger cho mobile */}
      <div
        className="mobile-menu-icon"
        onClick={() => setShowMobileMenu(!showMobileMenu)}
      >
        <i className="fa fa-bars"></i>
      </div>

      {/* Menu ngang cho tablet & desktop */}
      <ul className="nav-list">
        <li><a href="/">Home</a></li>
        <li><a href="/leaderboard">Leaderboard</a></li>
        <li><a href="/luckywheel">Upgrade</a></li>

        {user ? (
          <li className="nav-user" onClick={handleUserClick}>
            {user} {/* Hiển thị tên người dùng */}
            {showDropdown && (
              <div className="dropdown-menu">
                <a href="#!" onClick={handleLogout}>Đăng xuất</a>
                <a href="/user">Thông tin người dùng</a>
              </div>
            )}
          </li>
        ) : (
          <li><a href="/login">Login</a></li>
        )}
      </ul>

      {/* Menu dropdown cho mobile */}
      {showMobileMenu && (
        <div className="mobile-dropdown">
          <li><a href="/">Home</a></li>
          <li><a href="#about">Leaderboard</a></li>
          <li><a href="#mini-games">Mini-games</a></li>
          {user ? (
            <li className="nav-user" onClick={handleUserClick}>
              {user}
              {showDropdown && (
                <div className="dropdown-menu">
                  <a href="#!" onClick={handleLogout}>Đăng xuất</a>
                  <a href="/user">Thông tin người dùng</a>
                </div>
              )}
            </li>
          ) : (
            <li><a href="/login">Login</a></li>
          )}
        </div>
      )}
    </div>
  );
};

export default Navbar;
