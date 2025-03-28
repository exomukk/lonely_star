import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar/NavBar';
import HomePage from './components/homepage/main';
import Login from './components/login/login';
import Register from './components/register/register';
import UserProfile from './components/userprofile/UserProfile';
import PayMoney from './components/paymoney/PayMoney';

function App() {
  return (
    <Router>
      <div className="container" style={{ minHeight: '100vh' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user" element={<UserProfile />} />
          <Route path="/paymoney" element={<PayMoney />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
