import React, { useState } from 'react';
import Navbar from './components/navbar/NavBar'; // Import Navbar component

function App() {

  const [theme, setTheme] = useState('light');

  return (
    <div className={`container ${theme}`}>
      <Navbar theme={theme} setTheme={setTheme}/>
      <h1>Welcome to My React App</h1>
    </div>
  );
}

export default App;

