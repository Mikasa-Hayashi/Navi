import { useRef, useState, useEffect } from 'react';


function Login() {
    const userRef = useRef();
    const errorRef = useRef();
    
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrorMessage('');
    }, [username, password])

    return (
        <section>
            <p ref={errorRef} className={errorMessage ? "error-message" : "offscreen"} aria-live="assertive">{errorMessage}</p>
            <h1>Sign In</h1>
            <form >
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
            </form>
        </section>
    )
}

export default Login;