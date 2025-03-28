import React, { useState } from 'react';
import './NavBar.css';

const Navbar = () => {
  // Giả lập user state: null = chưa đăng nhập, 'béo' = đã đăng nhập
  const [user, setUser] = useState('béo');
  // const [user, setUser] = useState(null);

  const [showDropdown, setShowDropdown] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  const handleUserClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleLogout = () => {
    // Logic đăng xuất thật có thể là xóa token, gọi API, ...
    setUser(null);
    setShowDropdown(false);
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
        <li><a href="#about">Leaderboard</a></li>
        <li><a href="#mini-games">Mini-games</a></li>

        {user ? (
          <li className="nav-user" onClick={handleUserClick}>
            {user}
            {/* Dropdown hiển thị khi showDropdown = true */}
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
