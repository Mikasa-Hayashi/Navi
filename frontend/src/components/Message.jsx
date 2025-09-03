

function Message({ message }) {
    return (
        <div className={`message ${message.sender_type === 'user' ? 'user-message' : 'companion-message'}`}>
            <p>{message.content}</p>
        </div>
    )
}

export default Message;