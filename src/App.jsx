import React from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import RoleGrid from './components/skills/RoleGrid';

function App() {
  return (
    <ThemeProvider>
      <RoleGrid />
    </ThemeProvider>
  );
}

export default App;
