import { Link } from 'react-router-dom';

function Settings() {
    return (
        <div className="settings-page">
            <p>There will be settings page</p>
            <Link to="/chat">Chat</Link>
        </div>
    );
}

export default Settings;