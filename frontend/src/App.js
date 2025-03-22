import React, { useEffect, useState } from 'react';
import Navbar from './components/navbar/NavBar'; // Import Navbar component
import HomePage from './components/homepage/main'; // Import HomePage component

function App() {

  const current_theme = localStorage.getItem('theme');
  const [theme, setTheme] = useState(current_theme ? current_theme : 'light');

  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <div className={`container ${theme}`} style={{ minHeight: '100vh' }}>
      <Navbar theme={theme} setTheme={setTheme}/>
      <HomePage />
    </div>
  );
}

export default App;

