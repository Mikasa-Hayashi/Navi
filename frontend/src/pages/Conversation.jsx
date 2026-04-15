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
    const [conversation, setConversation] = useState(null);
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();
    const location = useLocation();
    const chatSocket = useRef(null);
    const messageEndRef = useRef(null);

    const scrollToBottom = () => {
        messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages])

    useEffect(() => {
        const fetchConversationData = async () => {
            try {
                const [conversationResponse, messagesResponse] = await Promise.all([
                    axiosPrivate.get(`/api/v1/conversations/${conversationId}/`),
                    axiosPrivate.get(`/api/v1/conversations/${conversationId}/messages/`),
                ]);
                setConversation(conversationResponse.data);
                setMessages(messagesResponse.data);
            } catch (error) {
                console.error(error);
                navigate('/login', { state: { from: location }, replace: true });
            }
        };

        fetchConversationData();
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

    const deleteChat = async () => {
        if (!window.confirm('Delete this chat history and unpair this companion?')) {
            return;
        }

        try {
            await axiosPrivate.delete(`/api/v1/conversations/${conversationId}/`);
            navigate('/chat', { replace: true });
        } catch (error) {
            console.error(error);
            setErrorMessage(error?.response?.data?.detail || 'Could not delete chat');
        }
    };

    return (
        <div className="conversation-page">
            <div className="conversation-header">
                <Link to="/chat">Back to chats</Link>
                <div className="conversation-actions">
                    <span className="conversation-companion-name">{conversation?.title || 'Conversation'}</span>
                    <button className="danger-button" type="button" onClick={deleteChat}>
                        Delete Chat
                    </button>
                </div>
            </div>
            {errorMessage ? <p className="error-message">{errorMessage}</p> : null}
            {/* <h2>Conversation { params.uuid }</h2> */}
            <div className="message-container">
                {messages.map(message => (
                    <Message className="message" message={message} key={message.id} />
                ))}
                <div ref={messageEndRef} />
            </div>
            <SendMessageBar className="send-message-bar" onSendMessage={sendMessage} companionName={conversation?.title || 'Companion'} />
        </div>
    )
}

export default Conversation;