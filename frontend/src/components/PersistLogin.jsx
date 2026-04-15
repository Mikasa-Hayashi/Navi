import { Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
import useRefreshToken from '../hooks/useRefreshToken';
import useAuth from '../hooks/useAuth';

const PersistLogin = () => {
    const [isLoading, setIsLoading] = useState(true);
    const refresh = useRefreshToken();
    const { auth } = useAuth();

    useEffect(() => {
        const persisted = localStorage.getItem('persist') === 'true';

        let isMounted = true;

        const verifyRefreshToken = async () => {
            try {
                await refresh();
            } catch (error) {
                console.error(error);
            } finally {
                if (isMounted) {
                    setIsLoading(false);
                }
            }
        };

        if (!auth?.accessToken && persisted) {
            verifyRefreshToken();
        } else {
            setIsLoading(false);
        }

        return () => {
            isMounted = false;
        };
    }, [auth?.accessToken, refresh]);

    if (isLoading) {
        return <p className="auth-loading">Restoring session...</p>;
    }

    return <Outlet />;
};

export default PersistLogin;
