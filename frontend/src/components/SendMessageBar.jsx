import { useState, useRef, useEffect } from 'react';
import '../css/SendMessageBar.css';

function SendMessageBar({ onSendMessage, companionName}) {
    const [message, setMessage] = useState('');
    const messageBarRef = useRef();

    useEffect(() => {
        messageBarRef.current.focus();
    }, [])

    const handleSubmit = (event) => {
        event.preventDefault();
        if (message && message.trim() !== '') {
            onSendMessage(message);
            setMessage('');
        }

    }
    return (
        <form className="send-message-bar-form" onSubmit={handleSubmit}>
            <textarea 
                className="send-message-input"
                name="message" 
                id="message" 
                placeholder={`Type to ${companionName}`} 
                value={message} 
                onChange={(event) => setMessage(event.target.value)}
                ref={messageBarRef}
                autoComplete="off"
                required
            ></textarea>
            <button className="send-message-button" type="submit">Send</button>
        </form>
    )
}

export default SendMessageBar;