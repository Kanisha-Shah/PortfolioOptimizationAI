import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/AskName.module.css';

const AskName = () => {
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) {
      localStorage.setItem('user', name.trim());
      navigate('/auth');
    }
  };

  return (
    <div className={styles.askName}>
      <div className={styles.formContainer}>
        <h2>Lets get started.. </h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Whats your good name?"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <button type="submit">Next</button>
        </form>
      </div>
    </div>
  );
};

export default AskName;