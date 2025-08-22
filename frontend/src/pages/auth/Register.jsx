import { useRef, useState, useEffect } from 'react';


const USER_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{3, 23}$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8, 24}$/;


function Register() {
    const userRef = useRef();
    const errRef = useRef();

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

    return (
        <div>
            Register
        </div>
    )
}

export default Register;