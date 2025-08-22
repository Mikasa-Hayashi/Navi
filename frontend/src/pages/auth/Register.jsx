import { useRef, useState, useEffect } from 'react';


const USER_REGEX = /^[a-zA-Z][a-zA-Z0-9-_]{3, 23}$/;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8, 24}$/;


function Register() {
    return (
        <div>
            Register
        </div>
    )
}

export default Register;