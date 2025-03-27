import React from 'react';
import { motion } from 'framer-motion';
import styles from '../styles/Landing.module.css'; 

const Hero = ({ onGetStarted }) => {
  return (
    <div className={styles.hero}>
      <div className={styles.heroContent}>
        <motion.button 
          className={styles.getStartedButton} 
          onClick={onGetStarted}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
        >
          Get Started
        </motion.button>
      </div>
    </div>
  );
};

export default Hero;