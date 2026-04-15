import { useEffect, useMemo, useState } from 'react';
import useAxiosPrivate from '../hooks/useAxiosPrivate';
import { useNavigate, useLocation } from 'react-router-dom';

const MAX_COMPANIONS = 2;

function Companion() {
    const axiosPrivate = useAxiosPrivate();
    const navigate = useNavigate();
    const location = useLocation();
    const [companions, setCompanions] = useState([]);
    const [conversations, setConversations] = useState([]);
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [name, setName] = useState('');
    const [avatar, setAvatar] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const loadData = async () => {
        try {
            const [companionsResponse, conversationsResponse] = await Promise.all([
                axiosPrivate.get('/api/v1/companions/'),
                axiosPrivate.get('/api/v1/conversations/'),
            ]);
            setCompanions(companionsResponse.data);
            setConversations(conversationsResponse.data);
        } catch (error) {
            console.error(error);
            navigate('/login', { state: { from: location }, replace: true });
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const companionConversationMap = useMemo(() => {
        const map = new Map();
        conversations.forEach((conversation) => {
            map.set(conversation.companion_id, conversation.id);
        });
        return map;
    }, [conversations]);

    const handleCreateCompanion = async (event) => {
        event.preventDefault();
        setErrorMessage('');
        try {
            await axiosPrivate.post('/api/v1/companions/', {
                name: name.trim(),
                avatar: avatar.trim(),
            });
            setName('');
            setAvatar('');
            setShowCreateForm(false);
            await loadData();
        } catch (error) {
            console.error(error);
            setErrorMessage(error?.response?.data?.detail || 'Could not create companion');
        }
    };

    const handleDeleteCompanion = async (companion) => {
        const hasChat = companionConversationMap.has(companion.id);
        const warningMessage = hasChat
            ? `Delete ${companion.name}? The chat with this companion will also be deleted.`
            : `Delete ${companion.name}?`;

        if (!window.confirm(warningMessage)) {
            return;
        }

        try {
            await axiosPrivate.delete(`/api/v1/companions/${companion.id}`);
            await loadData();
        } catch (error) {
            console.error(error);
            setErrorMessage(error?.response?.data?.detail || 'Could not delete companion');
        }
    };

    return (
        <div className="settings-page">
            <div className="page-header-row">
                <h2>Companions</h2>
            </div>

            {errorMessage ? <p className="error-message">{errorMessage}</p> : null}

            <ul className="companion-list">
                {companions.map((companion) => (
                    <li className="companion-item" key={companion.id}>
                        <div className="companion-item-main">
                            <img className="companion-item-avatar" src={companion.avatar} alt={`${companion.name} avatar`} />
                            <div className="companion-item-name">{companion.name}</div>
                        </div>
                        <button
                            className="danger-button"
                            type="button"
                            onClick={() => handleDeleteCompanion(companion)}
                        >
                            Delete
                        </button>
                    </li>
                ))}

                {companions.length < MAX_COMPANIONS ? (
                    <li className="companion-add-banner" onClick={() => setShowCreateForm(true)}>
                        <div className="companion-add-icon">+</div>
                        <div className="companion-add-text">Add a companion</div>
                    </li>
                ) : null}
            </ul>

            {showCreateForm ? (
                <form className="create-companion-form" onSubmit={handleCreateCompanion}>
                    <h3>Create companion</h3>
                    <div className="form-group">
                        <label className="form-label" htmlFor="companion-avatar">Avatar URL</label>
                        <input
                            id="companion-avatar"
                            className="form-input"
                            type="url"
                            value={avatar}
                            onChange={(event) => setAvatar(event.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label" htmlFor="companion-name">Name</label>
                        <input
                            id="companion-name"
                            className="form-input"
                            type="text"
                            value={name}
                            onChange={(event) => setName(event.target.value)}
                            required
                        />
                    </div>
                    <div className="button-row">
                        <button className="form-submit-button" type="submit">Add</button>
                        <button className="ghost-button" type="button" onClick={() => setShowCreateForm(false)}>
                            Cancel
                        </button>
                    </div>
                </form>
            ) : null}
        </div>
    )
}

export default Companion;