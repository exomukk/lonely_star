import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    password: ''
  });

  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Cập nhật giá trị input khi người dùng nhập
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Xử lý sự kiện khi người dùng gửi form
  const handleSubmit = async (e) => {
    console.log(formData);
    e.preventDefault();

    // Gửi request register đến server
    try {
      const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.status === 200) {
        setSuccessMessage('Registration successful! Please check your email for verification.');
        setErrorMessage('');
      } else {
        setErrorMessage(result.message || 'Registration failed. Please try again.');
        setSuccessMessage('');
      }
    } catch (error) {
      setErrorMessage(error.message || 'An error occurred. Please try again.');
      setSuccessMessage('');
    }
  };

  return (
    <div className="register-container">
      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register</h2>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
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
        <button type="submit">Register</button>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
};

export default Register;
