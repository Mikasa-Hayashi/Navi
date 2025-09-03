import ConversationItem from '../components/ConversationItem';
import useAuth from '../hooks/useAuth';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Link } from 'react-router-dom';

function Chat() {
    const { auth } = useAuth();
    const axiosPrivate = useAxiosPrivate();
    const [conversations, setConversations] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    // const conversations = [
    //     {id: 1, title: 'Navi'},
    //     {id: 2, title: 'Jade'},
    //     {id: 3, title: 'Joi'},
    // ];

    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const response = await axiosPrivate.get('/api/v1/chat/', {
                    'user': auth?.username
                });
                setConversations(response.data);
            } catch (error) {
                console.error(error);
                navigate('/login', { state: { from: location }, replace: true });
            }
        }

        fetchConversations();
    }, [])

    return (
        <div className="chat-page">
            <ul className="conversation-list">
                {conversations.map(conversation => (
                    <ConversationItem conversation={conversation} key={conversation.id} />
                ))}
            </ul>
        </div>
    );
}

export default Chat;