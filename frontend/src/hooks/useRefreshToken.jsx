import axios from '../api/axios';
import useAuth from './useAuth';

const parseJwtPayload = (token) => {
    try {
        const base64Payload = token.split('.')[1];
        return JSON.parse(atob(base64Payload));
    } catch {
        return {};
    }
};

const useRefreshToken = () => {
    const { setAuth } = useAuth();

    const refresh = async () => {
        const response = await axios.post('/api/v1/users/token/refresh', {}, {
            withCredentials: true
        });
        const accessToken = response.data.accessToken;
        const payload = parseJwtPayload(accessToken);

        setAuth(prev => {
            return {
                ...prev,
                username: payload.username || prev?.username,
                accessToken,
            };
        });
        return accessToken;
    }

    return refresh;
}

export default useRefreshToken;