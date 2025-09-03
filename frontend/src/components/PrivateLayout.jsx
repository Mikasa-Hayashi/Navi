import { Outlet } from 'react-router-dom';
import BottomNavBar from './BottomNavBar';

const PrivateLayout = () => {
    return (
        <div>
            <main>
                <Outlet />
            </main>
            <BottomNavBar />
        </div>
    )
}

export default PrivateLayout;