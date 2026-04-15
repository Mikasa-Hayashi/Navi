import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import useAxiosPrivate from '../hooks/useAxiosPrivate';

function ConversationItem({conversation}) {
    const axiosPrivate = useAxiosPrivate();
    const [companion, setCompanion] = useState(null);
    useEffect(() => {
        const fetchCompanion = async () => {
            try {
                const response = await axiosPrivate.get(`api/v1/companions/${conversation.companion_id}`, {
                });
                setCompanion(response.data);
            } catch (error) {
                console.error(error);
            }
        }
        fetchCompanion();
    }, [])

    return (
        <li className="conversation-item">
            <Link className="conversation-item-link" to={`/chat/${conversation.id}`}>
                <div className="conversation-avatar">
                    <img src={companion?.avatar} />
                </div>
                <div className="conversation-title">
                    <h3 className="conversation-title">{conversation.title}</h3>
                </div>
                <div className="conversation-last-message">
                    <p className="conversation-last-message-text">
                        {conversation.last_message ? conversation.last_message.content : 'No messages yet. Say hi!'}
                    </p>
                </div>
                <div className="conversation-timestamp">
                    <span className="conversation-timestamp-text">
                        {conversation.last_message ? new Date(conversation.last_message.timestamp).toLocaleString() : ''}
                    </span>
                </div>
            </Link>
        </li>
    );
}

export default ConversationItem;