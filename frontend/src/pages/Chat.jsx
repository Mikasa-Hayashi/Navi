import ConversationItem from '../components/ConversationItem';

function Chat() {
    const conversations = [
        {id: 1, title: 'Navi'},
        {id: 2, title: 'Jade'},
        {id: 3, title: 'Joi'},
    ];
    return (
        <div className="chat-page">
            <div className="conversation-list">
                {conversations.map(conversation => (
                    <ConversationItem conversation={conversation} key={conversation.id} />
                ))}
            </div>
        </div>
    );
}

export default Chat;