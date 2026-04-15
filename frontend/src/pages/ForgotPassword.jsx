import { Link } from "react-router-dom";

function ForgotPassword() {
    return (
        <section>
            <div className="info-card">
                <h1>Forgot Password</h1>
                <p>Please contact website developer:</p>
                <p><a href="https://web.telegram.org/k/#@Hayashi_ID">Ivan</a></p>
                <Link to="/login" className="form-link">Back to login page</Link>
            </div>
        </section>
    )
}

export default ForgotPassword;