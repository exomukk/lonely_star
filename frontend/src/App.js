import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar/NavBar';
import HomePage from './components/homepage/HomePage';
import Login from './components/login/login';
import Register from './components/register/register';
import UserProfile from './components/userprofile/UserProfile';
import PayMoney from './components/paymoney/PayMoney';
import Leaderboard from './components/leaderboard/leaderboard';
import LuckyWheel from './components/luckywheel/luckyWheel';
import OpenCase from './components/opencase/OpenCase';

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
