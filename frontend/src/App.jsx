import './App.css';
import Chat from './pages/Chat';
import Settings from './pages/Settings'
import Register from './pages/Register';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import Layout from './components/Layout';
import RequireAuth from './components/RequireAuth';
import { Routes, Route, Navigate } from 'react-router-dom';
import PrivateLayout from './components/PrivateLayout';
import Conversation from './pages/Conversation';
import Companion from './pages/Companion';


function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Navigate to="/login" replace />} />
        {/* public routes */}
        <Route path="register" element={<Register />} />
        <Route path="login" element={<Login />} />
        <Route path="forgot-password" element={<ForgotPassword />} />

        {/* private routes */}
        <Route element={<RequireAuth />} >
          <Route element={<PrivateLayout />} > {/*with navbar */}
            <Route path="chat" element={<Chat />} />
            <Route path="companion" element={<Companion />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          <Route path="chat/:uuid" element={<Conversation />} />
        </Route>

        {/* other */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Route>
    </Routes>
  )
}

export default App;
