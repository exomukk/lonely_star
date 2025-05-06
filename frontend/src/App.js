import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar/NavBar.jsx';
import HomePage from './components/homepage/HomePage.jsx';
import Login from './components/login/login.jsx';
import Register from './components/register/register.jsx';
import UserProfile from './components/userprofile/UserProfile.jsx';
import PayMoney from './components/paymoney/PayMoney.jsx';
import Leaderboard from './components/leaderboard/leaderboard.jsx';
import LuckyWheel from './components/luckywheel/luckyWheel.jsx';
import OpenCase from './components/opencase/OpenCase.jsx';

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
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/luckywheel" element={<LuckyWheel />} />
          <Route path="/opencase/:caseId" element={<OpenCase />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
