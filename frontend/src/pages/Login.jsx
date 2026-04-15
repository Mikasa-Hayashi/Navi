import { useRef, useState, useEffect } from 'react';
import axios from '../api/axios';
import useAuth from '../hooks/useAuth';
import { Link, useNavigate, useLocation } from 'react-router-dom';
// import '../css/Login.css';

const LOGIN_URL = '/api/v1/users/login/';

function Login() {
    const { setAuth } = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || '/chat';

    const userRef = useRef();
    const errorRef = useRef();
    
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [persist, setPersist] = useState(() => localStorage.getItem('persist') === 'true');

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrorMessage('');
    }, [username, password])

    useEffect(() => {
        localStorage.setItem('persist', persist);
    }, [persist]);

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post(
                LOGIN_URL, 
                JSON.stringify({ username, password, rememberMe: persist }),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                }
            );
            const accessToken = response?.data?.accessToken;  
            
            // roles
            setAuth({ username, accessToken });
            setUsername('');
            setPassword('');
            
            navigate(from, { replace: true });
        } catch (error) {
            if (!error?.response) {
                setErrorMessage('No Server Response');
            } else if (error.response?.status === 400) {
                setErrorMessage('Missing Username or Password');
            } else if (error.response?.status === 401) {
                setErrorMessage('Unauthorized');
            } else {
                setErrorMessage('Login Failed');
            }
            errorRef.current.focus();
        }
    }

    return (
        <section className="login-section">
            {/* Login header */}
            <div className="form-header login-header">
                <h1 className="form-title login-title">Sign In</h1>
                <p ref={errorRef} className={errorMessage ? "error-message" : "offscreen"} aria-live="assertive">{errorMessage}</p>
            </div>

            {/* Login form */}
            <form onSubmit={handleSubmit} className="form login-form">
                {/* Username */}
                <div className="form-group">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input 
                        type="text"
                        id="username"
                        className="form-input"
                        placeholder="Username"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(event) => setUsername(event.target.value)}
                        value={username}
                        required
                    />
                    <p></p>
                </div>

                {/* Password */}
                <div className="form-group">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input 
                        type="password"
                        id="password"
                        className="form-input"
                        placeholder="Password"
                        onChange={(event) => setPassword(event.target.value)}
                        value={password}
                        required
                    />
                </div>

                {/* Remember me */}
                <div className="form-group form-remember-me">
                    <input
                        id="remember-me"
                        type="checkbox"
                        className="form-checkbox"
                        checked={persist}
                        onChange={(event) => setPersist(event.target.checked)}
                    />
                    <label htmlFor="remember-me" className="form-label">
                        Remember me
                    </label>
                </div>

                {/* Forgot password */}
                <div className="form-group form-forgot-password">
                    <Link to="/forgot-password" className="form-link">Forgot password?</Link>
                </div>
                
                {/* Submit */}
                <div className="form-submit login-submit">
                    <button type="submit" className="form-submit-button">Sign In</button>
                </div>    
            </form>

            {/* Login footer */}
            <div className="form-footer login-footer">
                <p className="form-text register-text">
                    Don't have an account?
                    <Link to="/register" className="form-link">Sign Up</Link>
                </p>
            </div>
        </section>
    )
}

export default Login;