import React from 'react';
import { Link } from 'react-router-dom';
import './login.css';

const Login = () => {
  const [formData, setFormData] = React.useState({
    username: '',
    password: ''
  });

  const [errorMessage, setErrorMessage] = React.useState('');
  const [successMessage, setSuccessMessage] = React.useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData),
        credentials: 'include'
      });

      const result = await response.json();
      console.log(result);

      if (result.status === 'success') {
        setSuccessMessage('Login successful! Redirecting...');
        setErrorMessage('');
        window.location.href = '/';
      } else {
        setErrorMessage(result.message || 'Login failed. Please try again.');
        setSuccessMessage('');
      }
    } catch (error) {
      setErrorMessage(error.message || 'An error occurred. Please try again.');
      setSuccessMessage('');
    }
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleInputChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
        
        <button type="submit">Login</button>
        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
