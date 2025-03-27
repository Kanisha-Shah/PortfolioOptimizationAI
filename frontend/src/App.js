import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './components/Landing';
import AskName from './components/AskName';
import Auth from './components/Auth';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  // Whenever token changes, sync with localStorage
  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    }
  }, [token]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Landing />} />
        <Route path="/landing" element={token ? <Navigate to="/dashboard" /> : <Landing />} />
        <Route path="/ask-name" element={token ? <Navigate to="/dashboard" /> : <AskName />} />
        <Route path="/auth" element={<Auth onToken={setToken} />} />
        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/auth" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;