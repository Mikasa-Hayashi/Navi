import ConversationItem from '../components/ConversationItem';
import useAuth from '../hooks/useAuth';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const MAX_CHATS = 2;

function Chat() {
    const { auth } = useAuth();
    const axiosPrivate = useAxiosPrivate();
    const [conversations, setConversations] = useState([]);
    const [companions, setCompanions] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [showCompanionPicker, setShowCompanionPicker] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    
    const loadData = async () => {
        try {
            const [conversationsResponse, companionsResponse] = await Promise.all([
                axiosPrivate.get('/api/v1/conversations/', {
                    'user': auth?.username
                }),
                axiosPrivate.get('/api/v1/companions/'),
            ]);
            setConversations(conversationsResponse.data);
            setCompanions(companionsResponse.data);
            setErrorMessage('');
        } catch (error) {
            console.error(error);
            navigate('/login', { state: { from: location }, replace: true });
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const activeCompanionIds = new Set(conversations.map((conversation) => conversation.companion_id));
    const availableCompanions = companions.filter((companion) => !activeCompanionIds.has(companion.id));
    const emptySlotsCount = companions.length > 0 ? Math.max(MAX_CHATS - conversations.length, 0) : 0;

    const startChatWithCompanion = async (companionId) => {
        try {
            const response = await axiosPrivate.post('/api/v1/conversations/', {
                companion_id: companionId,
            });
            navigate(`/chat/${response.data.id}`);
        } catch (error) {
            console.error(error);
            setErrorMessage(error?.response?.data?.detail || 'Could not start chat');
        }
    };

    return (
        <div className="chat-page">
            <div className="page-header-row">
                <h2>Chats</h2>
            </div>
            {errorMessage ? <p className="error-message">{errorMessage}</p> : null}

            {companions.length === 0 ? (
                <div className="empty-state-banner">
                    <p className="empty-state-title">You do not have any companions yet.</p>
                    <p>Create one to start chatting.</p>
                    <button className="form-submit-button" onClick={() => navigate('/companion')}>
                        Create Companion
                    </button>
                </div>
            ) : null}

            <h3 className="section-title">Active Chats</h3>
            <ul className="conversation-list">
                {conversations.map(conversation => (
                    <ConversationItem conversation={conversation} key={conversation.id} />
                ))}
                {Array.from({ length: emptySlotsCount }).map((_, index) => (
                    <li
                        className="chat-slot clickable"
                        key={`chat-slot-${index}`}
                        onClick={() => setShowCompanionPicker(true)}
                    >
                        <div className="chat-slot-plus">+</div>
                        <div className="chat-slot-text">Click to assign companion</div>
                    </li>
                ))}
            </ul>

            {showCompanionPicker ? (
                <div className="picker-overlay" onClick={() => setShowCompanionPicker(false)}>
                    <div className="picker-modal" onClick={(event) => event.stopPropagation()}>
                        <h3>Select companion</h3>
                        {availableCompanions.length === 0 ? (
                            <p className="empty-state-inline">No available companions for a new chat.</p>
                        ) : (
                            <ul className="available-companion-list">
                                {availableCompanions.map((companion) => (
                                    <li className="available-companion-item" key={companion.id}>
                                        <div className="available-companion-main">
                                            <img src={companion.avatar} alt={`${companion.name} avatar`} />
                                            <span>{companion.name}</span>
                                        </div>
                                        <button
                                            className="form-submit-button"
                                            type="button"
                                            onClick={async () => {
                                                await startChatWithCompanion(companion.id);
                                                setShowCompanionPicker(false);
                                            }}
                                        >
                                            Start Chat
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        )}
                        <button className="ghost-button" type="button" onClick={() => setShowCompanionPicker(false)}>
                            Close
                        </button>
                    </div>
                </div>
            ) : null}
        </div>
    );
}

export default Chat;