import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
// import './App.css';
import Chat from './pages/Chat';
import Settings from './pages/Settings'
import BottomNavBar from './components/BottomNavBar';
import Register from './pages/auth/Register';
import Login from './pages/auth/Login';
import Layout from './components/Layout';
import RequireAuth from './components/RequireAuth';
import { Routes, Route } from 'react-router-dom';
import PrivateLayout from './components/PrivateLayout';
import Conversation from './pages/Conversation';


function App() {
  const [count, setCount] = useState(0);

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* public routes */}
        <Route path="register" element={<Register />} />
        <Route path="login" element={<Login />} />

        {/* private routes */}
        <Route element={<RequireAuth />} >
          <Route element={<PrivateLayout />} >
            <Route path="chat" element={<Chat />} />
            <Route path="chat/:uuid" element={<Conversation />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Route>

        {/* other */}
        {/* <Route path="*" element={<Missing />} /> */}
      </Route>
    </Routes>
  )
}

export default App;
