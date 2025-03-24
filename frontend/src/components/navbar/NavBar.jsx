import React, { useState } from 'react';
import './NavBar.css';
import toggle_light from '../../assets/Navbar_React_Assets/night.png';
import toggle_dark from '../../assets/Navbar_React_Assets/day.png';

const Navbar = ({ theme, setTheme }) => {
  // Giả lập user state: null = chưa đăng nhập, 'béo' = đã đăng nhập
  const [user, setUser] = useState('béo'); 
  // const [user, setUser] = useState(null);

  const [showDropdown, setShowDropdown] = useState(false);

  const handleUserClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleLogout = () => {
    // Logic đăng xuất thật có thể là xóa token, gọi API, ...
    setUser(null);
    setShowDropdown(false);
  };

  const toggleTheme = () => {
    if (theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  }

  return (
    <div className="navbar">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="#about">Leaderboard</a></li>
        <li><a href="#mini-games">Mini-games</a></li>
        {/* <li><a href="/login">Login</a></li> */}

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

      <img onClick={() => { toggleTheme() }} src={theme === 'light' ? toggle_light : toggle_dark} alt="" className="toggle-icon" />
    </div>
  );
};

export default Navbar;
