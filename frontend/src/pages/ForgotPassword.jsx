import { Link } from "react-router-dom";

function ForgotPassword() {
    return (
        <div>
            <p>Please contact website developer:</p> 
            <p><a href="https://web.telegram.org/k/#@Hayashi_ID">Ivan</a></p>
            <Link to="/login">Back to login page</Link>
        </div>
    )
}

export default ForgotPassword;