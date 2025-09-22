import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import '../css/ConversationItem.css';

function ConversationItem({conversation}) {
    const axiosPrivate = useAxiosPrivate();
    const [companion, setCompanion] = useState(null);
    useEffect(() => {
        const fetchCompanion = async () => {
            try {
                const response = await axiosPrivate.get(`api/v1/companion/${conversation.companion_id}`, {
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
            <Link to={`/chat/${conversation.id}`}>
                <div className="conversation-avatar">
                    <img src={companion?.avatar} />
                </div>
                <div className="conversation-title">
                    <h3 className="conversation-title">{conversation.title}</h3>
                </div>
                <div className="conversation-last-message">

                </div>
                <div className="conversation-timestamp">

                </div>
            </Link>
        </li>
    );
}

export default ConversationItem;