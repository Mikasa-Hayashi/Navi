import { Outlet } from 'react-router-dom';

const Layout = () => {
    return (
        <main className="main-app">
            <Outlet />
        </main>
    )
}

export default Layout;