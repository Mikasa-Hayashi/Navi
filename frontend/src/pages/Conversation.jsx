import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Message from '../components/Message';
import { useState, useEffect, useRef } from 'react';
import useAuth from '../hooks/useAuth';
import { useNavigate, useLocation } from 'react-router-dom';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import SendMessageBar from '../components/SendMessageBar';

function Conversation() {
    const params = useParams();
    const conversationId = params.uuid;
    const { auth } = useAuth();
    const axiosPrivate = useAxiosPrivate();
    const [messages, setMessages] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const chatSocket = useRef(null);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await axiosPrivate.get(`/api/v1/chat/${conversationId}`, {
                    'conversation_id': conversationId
                });
                console.log(response.data);
                setMessages(response.data);
            } catch (error) {
                console.error(error);
                navigate('/login', { state: { from: location }, replace: true });
            }
        };

        fetchMessages();
    }, [])

    useEffect(() => {
        const url = `ws://localhost:8000/ws/chat/${conversationId}/`;
        chatSocket.current = new WebSocket(url);

        chatSocket.current.onmessage = function(event) {
            const data = JSON.parse(event.data);
            // console.log(data);

            if (data.message) {
                // console.log('Received message id: ', data.message.id);
                setMessages(prevMessages => [...prevMessages, data.message])
            }

        }

        return () => {
            chatSocket.current.close();
        }
    }, [])

    const sendMessage = (messageContent) => {
        console.log('sending message: ', messageContent);
        chatSocket.current.send(JSON.stringify({
            'message': messageContent
        }))
    }

    return (
        <div className="conversation-page">
            <Link to="/chat">Back to chats</Link>
            {/* <h2>Conversation { params.uuid }</h2> */}
            <div className="message-container">
                {messages.map(message => (
                    <Message message={message} key={message.id} />
                ))}
            </div>
            <SendMessageBar onSendMessage={sendMessage} companionName="Companion" />
        </div>
    )
}

export default Conversation;