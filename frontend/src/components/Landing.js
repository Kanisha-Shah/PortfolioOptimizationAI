import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Hero from './Hero';

const Landing = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/ask-name');
    }, 30000);
    return () => clearTimeout(timer);
  }, [navigate]);

  return <Hero onGetStarted={() => navigate('/ask-name')} />;
};

export default Landing;