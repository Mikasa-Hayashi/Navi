import { useRef, useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import axios from '../api/axios';


const USER_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{3,23}$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;
const REGISTER_URL = '/api/v1/users/register/';

function Register() {
    const userRef = useRef();
    const errorRef = useRef();

    const [user, setUser]  = useState('');
    const [validName, setValidName] = useState(false);
    const [userFocus, setUserFocus] = useState(false);

    const [password, setPassword]  = useState('');
    const [validPassword, setValidPassword] = useState(false);
    const [passwordFocus, setPasswordFocus] = useState(false);

    const [matchPassword, setMatchPassword]  = useState('');
    const [validMatch, setValidMatch] = useState(false);
    const [matchFocus, setMatchFocus] = useState(false);

    const [errorMessage, setErrorMessage] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        const result = USER_REGEX.test(user);
        console.log(result);
        console.log(user);
        setValidName(result);
    }, [user])

    useEffect(() => {
        const result = PASSWORD_REGEX.test(password);
        console.log(result);
        console.log(password);
        setValidPassword(result);
        const match = password === matchPassword;
        console.log(match);
        setValidMatch(match);
    }, [password, matchPassword])

    useEffect(() => {
        setErrorMessage('');
    }, [user, password, matchPassword])

    const handleSubmit = async (event) => {
        event.preventDefault();
        const v1 = USER_REGEX.test(user);
        const v2 = PASSWORD_REGEX.test(password);
        if (!v1 || !v2) {
            setErrorMessage('Invalid entry');
            return;
        }
        try {
            const response = await axios.post(
                REGISTER_URL,
                JSON.stringify({ username: user, password }),
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true
                }
            );
            setSuccess(true);
        } catch (error) {
            if (!error?.response) {
                setErrorMessage('No Server Response');
            } else if (error.response?.status === 409) {
                setErrorMessage('Username Taken')
            } else {
                setErrorMessage('Registration Failed')
            }
            errorRef.current.focus();
        }
    }

    return (
        <section>
            {/* Register header */}
            <div>
                <h1 className="form-header register-form">Sign Up</h1>
                <p ref={errorRef} className={errorMessage ? "error-message" : "offscreen"} aria-live="assertive">{errorMessage}</p>
            </div>

            {/* Register form */}
            <form onSubmit={handleSubmit} className="form register-form">
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
                        onChange={(event) => setUser(event.target.value)}
                        required
                        aria-invalid={validName ? "false" : "true"}
                        aria-describedby="uidnote"
                        onFocus={() => setUserFocus(true)}
                        onBlur={() => setUserFocus(false)}
                    />
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
                        required
                        aria-invalid={validPassword ? "false" : "true"}
                        aria-describedby="pwdnote"
                        onFocus={() => setPasswordFocus(true)}
                        onBlur={() => setPasswordFocus(false)}
                    />
                </div>

                {/* Confirm password */}
                <div className="form-group">
                    <label htmlFor="confirm-password" className="form-label">Confirm password</label>
                    <input
                        type="password"
                        id="confirm-password"
                        className="form-input"
                        placeholder="Confirm password"
                        onChange={(event) => setMatchPassword(event.target.value)}
                        required
                        aria-invalid={validPassword ? "false" : "true"}
                        aria-describedby="confirmnote"
                        onFocus={() => setMatchFocus(true)}
                        onBlur={() => setMatchFocus(false)}
                    />
                </div>

                {/* Submit */}
                <div className="form-submit register-submit">
                    <button type="submit" className="form-submit-button" disabled={!validName || !validPassword || !validMatch ? true : false}>
                        Sign Up
                    </button>
                </div>
            </form>

            {/* Register footer */}
            <div className="form-footer register-footer">
                <p className="form-text login-text">
                    Already have an account?
                    <Link to="/login" className="form-link">Sign In</Link>
                </p>
            </div>
        </section>
    )
}

export default Register;