import { Link } from 'react-router-dom';

function BottomNavBar() {
    return (
        <nav className="bottom-navigation-bar">
            <div>
                <Link className="navbar-link" to="/chat">Chat</Link>
                <Link className="navbar-link" to="/settings">Settings</Link>
            </div>
        </nav>
    )
}

export default BottomNavBar;