import React from 'react';
import './NavBar.css';
import toggle_light from '../../assets/Navbar_React_Assets/night.png';
import toggle_dark from '../../assets/Navbar_React_Assets/day.png';

const Navbar = ({theme, setTheme}) => {

  const toggleTheme = () => {
    if(theme === 'light') {
      setTheme('dark');
    } else {
      setTheme('light');
    }
  }

  return (
    <div className="navbar">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#mini-games">Mini-games</a></li>
        <li><a href="/login">Login</a></li>
      </ul>

      <img onClick={()=>{toggleTheme()}} src={theme === 'light' ? toggle_light : toggle_dark} alt="" className="toggle-icon" />
    </div>
  );
};

export default Navbar;
