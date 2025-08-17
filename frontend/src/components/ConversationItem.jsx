function ConversationItem({conversation}) {

    return (
        <div className="conversation-item">
            <div className="conversation-avatar">
                <img src={conversation.avatar} />
            </div>
            <div className="conversation-info">
                <h3 className="conversation-title">{conversation.title}</h3>
            </div>
        </div>
    );
}

export default ConversationItem;