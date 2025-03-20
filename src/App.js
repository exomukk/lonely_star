import React, { useEffect, useState } from 'react';
import Navbar from './components/navbar/NavBar'; // Import Navbar component

function App() {

  const current_theme = localStorage.getItem('theme');
  const [theme, setTheme] = useState(current_theme ? current_theme : 'light');

  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <div className={`container ${theme}`}>
      <Navbar theme={theme} setTheme={setTheme}/>
      <h1>Welcome to My React App</h1>
    </div>
  );
}

export default App;

