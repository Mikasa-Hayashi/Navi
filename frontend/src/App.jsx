import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import Chat from './pages/Chat';
import Settings from './pages/Settings'
import { Routes, Route } from 'react-router-dom'

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <main className="main-content">
        <Routes>
          <Route path="/chat" element={<Chat />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
