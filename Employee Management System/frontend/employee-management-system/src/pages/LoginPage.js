import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../services/apiService';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';  // Importing the CSS file for styling

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');  // Reset error message
    try {
      const response = await login(username, password);
      loginUser(response.data);

      if (response.data.role === 'admin') {
        navigate('/admin');
      } else if (response.data.role === 'manager') {
        navigate('/manager');
      } else if (response.data.role === 'user') {
        navigate('/user');
      } else {
        setError('Invalid role');
      }
    } catch (error) {
      setError('Login failed. Please check your username and password.');
      console.error('Login failed', error);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        <button type="submit" className="login-button">Login</button>
        <Link to="/change-password" className="change-password-link">
          Change Password
        </Link>
      </form>
    </div>
  );
};

export default LoginPage;
