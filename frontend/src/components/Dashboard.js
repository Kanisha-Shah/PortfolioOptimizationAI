import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../styles/Dashboard.module.css';

const Dashboard = () => {
  const token = localStorage.getItem('token');
  const storedUser = localStorage.getItem('user');

  const [userData, setUserData] = useState({
    name: storedUser || '',
    risk_tolerance: 'medium',
    goals: '',
    holdings: []
  });
  const [message, setMessage] = useState('');
  const [pdfUrl, setPdfUrl] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/user/${storedUser}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        }
      } catch (error) {
        console.error('Error fetching user data', error);
      }
    };
    if (storedUser) {
      fetchUserData();
    }
  }, [storedUser, token]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/landing');
  };

  const handleHoldingChange = (index, field, value) => {
    const updatedHoldings = [...userData.holdings];
    updatedHoldings[index][field] = field === 'symbol' ? value : parseFloat(value);
    setUserData({ ...userData, holdings: updatedHoldings });
  };

  const addHolding = () => {
    setUserData({
      ...userData,
      holdings: [...userData.holdings, { symbol: '', quantity: 0, purchase_price: 0 }]
    });
  };

  const removeHolding = (indexToRemove) => {
    setUserData({
      ...userData,
      holdings: userData.holdings.filter((_, index) => index !== indexToRemove)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Processing pipeline...');
    setPdfUrl('');
    try {
      const response = await fetch('http://127.0.0.1:8000/api/run-pipeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(userData)
      });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        setPdfUrl(url);
        setMessage('Pipeline executed successfully. PDF generated.');
      } else {
        const errorData = await response.json();
        setMessage('Error: ' + (errorData.detail || 'Pipeline failed'));
      }
    } catch (error) {
      setMessage('An error occurred during pipeline execution.');
    }
  };

  return (
    <div className={styles.dashboardContainer}>
      {/* Header with centered heading and logout on the right */}
      <div className={styles.header}>
        <h2>Dashboard</h2>
        <button className={styles.logoutButton} onClick={handleLogout}>Logout</button>
      </div>

      {/* Main content area: left = previous holdings, right = form */}
      <div className={styles.content}>
        {/* Previous Holdings in a table */}
        <div className={styles.previousHoldings}>
          <h3>Previous Holdings</h3>
          <br />
          {userData.holdings && userData.holdings.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Quantity</th>
                  <th>Purchase Price</th>
                </tr>
              </thead>
              <tbody>
                {userData.holdings.map((holding, index) => (
                  <tr key={index}>
                    <td>{holding.symbol}</td>
                    <td>{holding.quantity}</td>
                    <td>{holding.purchase_price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No holdings found</p>
          )}
        </div>

        {/* Add/Update Holdings Form */}
        <div className={styles.holdingsForm}>
          <h3>Add / Modify Holdings</h3>
          <br />
          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label>Risk Tolerance</label>
              <select
                value={userData.risk_tolerance}
                onChange={(e) =>
                  setUserData({ ...userData, risk_tolerance: e.target.value })
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div className={styles.formGroup}>
              <label>Investment Goals</label>
              <input
                value={userData.goals}
                onChange={(e) =>
                  setUserData({ ...userData, goals: e.target.value })
                }
              />
            </div>

            <div>
              <h4>Recent Holdings</h4>
              <br />
              {userData.holdings.map((holding, index) => (
                <div key={index} className={styles.formGroup}>
                  <input
                    type="text"
                    placeholder="Symbol"
                    value={holding.symbol}
                    onChange={(e) =>
                      handleHoldingChange(index, 'symbol', e.target.value)
                    }
                    required
                  />
                  <input
                    type="number"
                    placeholder="Quantity"
                    value={holding.quantity}
                    onChange={(e) =>
                      handleHoldingChange(index, 'quantity', e.target.value)
                    }
                    required
                  />
                  <input
                    type="number"
                    placeholder="Purchase Price"
                    value={holding.purchase_price}
                    onChange={(e) =>
                      handleHoldingChange(index, 'purchase_price', e.target.value)
                    }
                    required
                  />
                  <button
                    type="button"
                    onClick={() => removeHolding(index)}
          
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button type="button" onClick={addHolding}>
                Add Holding
              </button>
            </div>

            <button type="submit" style={{ marginTop: '9rem' }}>
              Run Pipeline
            </button>
          </form>
        </div>
      </div>

      {/* Status message and PDF link */}
      {message && <p className={styles.statusMessage}>{message}</p>}
      {pdfUrl && (
        <a href={pdfUrl} download="portfolio_report.pdf" className={styles.pdfLink}>
          Download PDF Report
        </a>
      )}
    </div>
  );
};

export default Dashboard;