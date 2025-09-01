import { useRef, useState, useEffect } from 'react';
import api from '../../services/api';
import useAuth from '../../hooks/useAuth';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const LOGIN_URL = '/api/v1/users/login/';

function Login() {
    const { setAuth } = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || '/';

    const userRef = useRef();
    const errorRef = useRef();
    
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrorMessage('');
    }, [username, password])

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await api.post(
                LOGIN_URL, 
                JSON.stringify({username, password}),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                }
            );
            const accessToken = response?.data?.accessToken;  
            
            // roles
            setAuth({ username, password, accessToken });
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
        <section>
            <p ref={errorRef} className={errorMessage ? "error-message" : "offscreen"} aria-live="assertive">{errorMessage}</p>
            <h1>Sign In</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input 
                        type="text"
                        id="username"
                        ref={userRef}
                        autoComplete="off"
                        onChange={(event) => setUsername(event.target.value)}
                        value={username}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input 
                        type="password"
                        id="password"
                        onChange={(event) => setPassword(event.target.value)}
                        value={password}
                        required
                    />
                </div>
                <button>Sign In</button>
            </form>
            <p>
                Need an account?<br />
                <span>
                    <a href="#">Sign Up</a>
                </span>
            </p>
        </section>
    )
}

export default Login;