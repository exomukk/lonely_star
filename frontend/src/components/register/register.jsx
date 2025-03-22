import React from 'react';
import { Link } from 'react-router-dom';
import './register.css';

const Register = () => {
  return (
    <div className="register-container">
      <form className="register-form">
        <h2>Register</h2>
        <input type="text" placeholder="Username" required />
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit">Register</button>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
};

export default Register;
