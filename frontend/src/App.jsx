import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';
import Chat from './pages/Chat';
import Settings from './pages/Settings'
import { Routes, Route } from 'react-router-dom';
import BottomNavBar from './components/BottomNavBar';
import Register from './pages/auth/Register';
import Login from './pages/auth/Login';



function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>
        <main className="main-content">
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <BottomNavBar />
      </div>
    </>
  );
}

export default App;
