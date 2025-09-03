import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Message from '../components/Message';
import { useState, useEffect } from 'react';
import useAuth from '../hooks/useAuth';
import { useNavigate, useLocation } from 'react-router-dom';
import useAxiosPrivate from '../hooks/useAxiosPrivate';

function Conversation() {
    const params = useParams();
    const conversationId = params.uuid;
    const { auth } = useAuth();
    const axiosPrivate = useAxiosPrivate();
    const [messages, setMessages] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axiosPrivate.get(`/api/v1/chat/${conversationId}`, {
                    'conversation_id': conversationId
                });
                setMessages(response.data);
            } catch (error) {
                console.error(error);
                navigate('/login', { state: { from: location }, replace: true });
            }
        };

        fetchMessages();
    }, [])

    return (
        <div className="conversation-page">
            <Link to="/chat">Back to chats</Link>
            {/* <h2>Conversation { params.uuid }</h2> */}
            <div className="message-container">
                {messages.map(message => (
                    <Message message={message} key={message.id} />
                ))}
            </div>
        </div>
    )
}

export default Conversation;