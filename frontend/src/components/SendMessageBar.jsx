import { useState, useRef, useEffect } from 'react';

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
        <form onSubmit={handleSubmit}>
            <div>
                <input 
                    type="text" 
                    name="message" 
                    placeholder={`Type to ${companionName}`}
                    required
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    autoComplete="off"
                    ref={messageBarRef}
                />
                <button type="submit">Send</button>
            </div>
        </form>
    )
}

export default SendMessageBar;