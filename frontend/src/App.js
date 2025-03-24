import React, { useEffect, useState } from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Navbar from './components/navbar/NavBar';
import HomePage from './components/homepage/main';
import Login from './components/login/login';
import Register from './components/register/register';
import UserProfile from './components/userprofile/UserProfile';

function App() {

  const current_theme = localStorage.getItem('theme');
  const [theme, setTheme] = useState(current_theme ? current_theme : 'light');

  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <Router>
      <div className={`container ${theme}`} style={{ minHeight: '100vh' }}>
        <Navbar theme={theme} setTheme={setTheme}/>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user" element={<UserProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

