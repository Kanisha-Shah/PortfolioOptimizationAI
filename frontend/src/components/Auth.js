// src/components/Auth.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/Auth.module.css';

const Auth = ({ onToken }) => {
  const storedName = localStorage.getItem('user') || '';
  const [submittedName] = useState(storedName);
  const [formType, setFormType] = useState('none'); // 'none', 'login', or 'register'
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [info, setInfo] = useState('');  // <-- For success or informational messages

  const navigate = useNavigate();

  // If there's already a token, go directly to dashboard
  useEffect(() => {
    if (localStorage.getItem('token')) {
      navigate('/dashboard');
    }
  }, [navigate]);

  // If the user’s name is missing, they probably skipped AskName.
  useEffect(() => {
    if (!submittedName) {
      navigate('/ask-name');
    }
  }, [submittedName, navigate]);

  // --- LOGIN HANDLER ---
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: submittedName, password })
      });
      if (response.ok) {
        const data = await response.json();
        onToken(data.access_token);
        navigate('/dashboard');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed');
        setInfo('');
      }
    } catch (err) {
      setError('An error occurred during login.');
      setInfo('');
    }
  };

  // --- REGISTER HANDLER ---
  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: submittedName, password })
      });
      if (response.ok) {
        setError('');
        setInfo('Registration successful. Please login below.');
        // Automatically switch to login form
        setFormType('login');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Registration failed');
        setInfo('');
      }
    } catch (err) {
      setError('An error occurred during registration.');
      setInfo('');
    }
  };

  // --- RENDER LOGIC ---
  if (formType === 'none') {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Hello, {submittedName}!</h2>
          <p>What would you like to do?</p>
          <button onClick={() => setFormType('login')}>Login</button>
          <button onClick={() => setFormType('register')}>Register</button>
        </div>
      </div>
    );
  }

  if (formType === 'login') {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Login for {submittedName}</h2>
          {info && <p className={styles.info}>{info}</p>}
          {error && <p className={styles.error}>{error}</p>}
          <form onSubmit={handleLogin}>
            <div>
              <label>Name</label>
              <input type="text" value={submittedName} disabled />
            </div>
            <div>
              <label>Password</label>
              <input 
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit">Login</button>
          </form>
        </div>
      </div>
    );
  }

  if (formType === 'register') {
    return (
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h2>Register for {submittedName}</h2>
          {error && <p className={styles.error}>{error}</p>}
          <form onSubmit={handleRegister}>
            <div>
              <label>Name</label>
              <input type="text" value={submittedName} disabled />
            </div>
            <div>
              <label>Password</label>
              <input 
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit">Register</button>
          </form>
        </div>
      </div>
    );
  }

  return null;
};

export default Auth;