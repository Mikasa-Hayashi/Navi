import api from '../services/api';
import useAuth from './useAuth';

const useRefreshToken = () => {
    const { setAuth } = useAuth();
    const refresh = async () => {
        const response = await api.get('/api/token/refresh', {
            WithCredentials: true
        });
        setAuth(prev => {
            console.log(JSON.stringify(prev));
            console.log(response.data.access);
            return { ...prev, accessToken: response.data.access };
        });
        return response.data.access;
    }
    return refresh;
}

export default useRefreshToken;