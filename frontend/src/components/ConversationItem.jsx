import { Link } from 'react-router-dom';

function ConversationItem({conversation}) {

    return (
        <li className="conversation-item">
            <Link to={`/chat/${conversation.id}`}>
                <div className="conversation-avatar">
                    <img src={conversation.avatar} />
                </div>
                <div className="conversation-info">
                    <h3 className="conversation-title">{conversation.title}</h3>
                </div>
            </Link>
        </li>
    );
}

export default ConversationItem;