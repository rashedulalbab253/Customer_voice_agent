document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const apiKeyInput = document.getElementById('apiKey');
    const userIdInput = document.getElementById('userId');
    const initBtn = document.getElementById('initAgent');
    const genProfileBtn = document.getElementById('genProfile');
    const viewMemoriesBtn = document.getElementById('viewMemories');
    const agentStatus = document.getElementById('agentStatus');
    const statusIndicator = document.querySelector('.status-indicator');
    const profileDisplay = document.getElementById('profileDisplay');
    const profileJson = document.getElementById('profileJson');

    const micBtn = document.getElementById('micBtn');
    const autoSpeakCheck = document.getElementById('autoSpeak');

    let initialized = false;
    let isRecording = false;

    // --- Voice Logic ---
    const recognition = window.SpeechRecognition || window.webkitSpeechRecognition ?
        new (window.SpeechRecognition || window.webkitSpeechRecognition)() : null;

    if (recognition) {
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            isRecording = true;
            micBtn.classList.add('recording');
            updateStatus(true, 'Listening...');
        };

        recognition.onend = () => {
            isRecording = false;
            micBtn.classList.remove('recording');
            updateStatus(true, 'Agent Online');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            isRecording = false;
            micBtn.classList.remove('recording');
        };
    }

    const speak = (text) => {
        if (!autoSpeakCheck.checked) return;

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        // Find a higher quality voice if available
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Premium')) || voices[0];
        if (preferredVoice) utterance.voice = preferredVoice;

        window.speechSynthesis.speak(utterance);
    };

    // --- Helper Functions ---

    const addMessage = (role, text) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = `<div class="bubble">${text}</div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const updateStatus = (online, message) => {
        initialized = online;
        agentStatus.textContent = message;
        if (online) {
            statusIndicator.classList.add('online');
        } else {
            statusIndicator.classList.remove('online');
        }
    };

    // --- API Calls ---

    const initializeAgent = async () => {
        const apiKey = apiKeyInput.value.trim();
        const userId = userIdInput.value.trim();

        if (!apiKey || !userId) {
            alert('Please provide both API Key and Customer ID');
            return;
        }

        updateStatus(false, 'Connecting...');

        // We'll just test a chat or assume it's fine for now 
        // In a real app, we might have a dedicated /init endpoint
        updateStatus(true, 'Agent Online');
        addMessage('assistant', `Agent initialized for customer: <strong>${userId}</strong>. How can I help you?`);
    };

    const sendMessage = async () => {
        const text = userInput.value.trim();
        const userId = userIdInput.value.trim();
        const apiKey = apiKeyInput.value.trim();

        if (!text) return;
        if (!initialized) {
            alert('Please initialize the agent first');
            return;
        }

        addMessage('user', text);
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text, user_id: userId, api_key: apiKey })
            });
            const data = await response.json();
            console.log("Server Response:", data);

            if (data.response) {
                addMessage('assistant', data.response);
                speak(data.response);
            } else if (data.detail) {
                addMessage('assistant', `Error: ${data.detail}`);
            } else {
                addMessage('assistant', "Error: Received undefined response from server.");
            }
        } catch (error) {
            addMessage('assistant', 'Error: Could not reach the server.');
        }
    };

    const generateProfile = async () => {
        const userId = userIdInput.value.trim();
        const apiKey = apiKeyInput.value.trim();

        if (!initialized) {
            alert('Please initialize first');
            return;
        }

        try {
            updateStatus(true, 'Generating Profile...');
            const response = await fetch('/generate-profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, api_key: apiKey })
            });
            const data = await response.json();
            profileDisplay.classList.remove('hidden');
            profileJson.textContent = JSON.stringify(data, null, 2);
            updateStatus(true, 'Agent Online');
            alert('Synthetic profile generated and added to memory!');
        } catch (error) {
            alert('Failed to generate profile');
            updateStatus(true, 'Agent Online');
        }
    };

    const fetchMemories = async () => {
        const userId = userIdInput.value.trim();
        if (!userId) {
            alert('Enter User ID first');
            return;
        }

        try {
            const response = await fetch(`/memories/${userId}`);
            const data = await response.json();

            const modal = document.getElementById('memoryModal');
            const list = document.getElementById('memoryList');
            list.innerHTML = '';

            if (data.memories.length === 0) {
                list.innerHTML = '<li>No memories found for this user.</li>';
            } else {
                data.memories.forEach(m => {
                    const li = document.createElement('li');
                    li.textContent = m;
                    list.appendChild(li);
                });
            }

            modal.classList.remove('hidden');
        } catch (error) {
            alert('Failed to fetch memories');
        }
    };

    // --- Event Listeners ---

    initBtn.addEventListener('click', initializeAgent);
    sendBtn.addEventListener('click', sendMessage);

    micBtn.addEventListener('click', () => {
        if (!recognition) {
            alert('Speech recognition is not supported in this browser.');
            return;
        }
        if (isRecording) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    genProfileBtn.addEventListener('click', generateProfile);
    viewMemoriesBtn.addEventListener('click', fetchMemories);

    // Modal close
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('memoryModal').classList.add('hidden');
    });

    // Clear chat
    document.getElementById('clearChat').addEventListener('click', () => {
        chatMessages.innerHTML = '';
        addMessage('assistant', 'Chat cleared.');
    });
});
