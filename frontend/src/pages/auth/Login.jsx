import { useRef, useState, useEffect } from 'react';


function Login() {
    const userRef = useRef();
    const errorRef = useRef();
    
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [success, setSuccess] = useState(false);

    return (
        <div></div>
    )
}

export default Login;