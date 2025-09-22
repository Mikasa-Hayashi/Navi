import { NavLink } from 'react-router-dom';
import '../css/BottomNavBar.css';

function BottomNavBar() {
    return (
        <nav className="bottom-navbar">
            <ul className="bottom-navbar-list">
                <li className="bottom-navbar-item">
                    <NavLink id="chat" className="bottom-navbar-item-link" to="/chat">
                        <div className="bottom-navbar-item-icon">

                        </div>
                        <span className="bottom-navbar-item-label">Chat</span>
                    </NavLink>    
                </li>
                <li className="bottom-navbar-item">
                    <NavLink id="model" className="bottom-navbar-item-link" to="/model">
                        <div className="bottom-navbar-item-icon">

                        </div>
                        <span className="bottom-navbar-item-label">3d</span>
                    </NavLink>
                </li>
                <li className="bottom-navbar-item">
                    <NavLink id="companions" className="bottom-navbar-item-link" to="/companion">
                        <div className="bottom-navbar-item-icon">

                        </div>
                        <span className="bottom-navbar-item-label">Companion</span>
                    </NavLink>
                </li>
                <li className="bottom-navbar-item">
                    <NavLink id="shop" className="bottom-navbar-item-link" to="/shop">
                        <div className="bottom-navbar-item-icon">

                        </div>
                        <span className="bottom-navbar-item-label">Shop</span>
                    </NavLink>
                </li>
                <li className="bottom-navbar-item">
                    <NavLink id="settings" className="bottom-navbar-item-link" to="/settings">
                        <div className="bottom-navbar-item-icon">

                        </div>
                        <span className="bottom-navbar-item-label">Settings</span>
                    </NavLink>
                </li>
            </ul>
        </nav>
    )
}

export default BottomNavBar;