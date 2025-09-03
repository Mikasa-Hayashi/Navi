import { useParams } from 'react-router-dom';

function Conversation() {
    const params = useParams();

    return (
        <div className="conversation-page">
            <h2>Conversation { params.uuid }</h2>
        </div>
    )
}

export default Conversation;