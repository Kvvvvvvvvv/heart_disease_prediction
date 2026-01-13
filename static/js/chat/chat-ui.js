// Chat UI Manager
class ChatUI {
    constructor(chatPanelId = 'chatPanel', messageContainerId = 'chatMessages', inputId = 'chatInput') {
        this.chatPanel = document.getElementById(chatPanelId);
        this.messageContainer = document.getElementById(messageContainerId);
        this.inputElement = document.getElementById(inputId);
        this.currentReceiverId = null;
        this.currentUserId = null; // Will be set when the app initializes
        this.typingTimeout = null;
    }

    // Initialize chat UI
    initialize() {
        if (!this.chatPanel || !this.messageContainer || !this.inputElement) {
            console.error('Chat UI elements not found');
            return;
        }

        // Set up event listeners
        this.setupEventListeners();
    }

    // Set current user ID
    setCurrentUserId(userId) {
        this.currentUserId = userId;
    }

    // Set current receiver ID
    setCurrentReceiverId(receiverId) {
        this.currentReceiverId = receiverId;
    }

    // Setup event listeners
    setupEventListeners() {
        // Send message on Enter key (without Shift)
        this.inputElement.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Typing indicator
        this.inputElement.addEventListener('input', () => {
            this.sendTypingIndicator();
        });
    }

    // Send a message
    async sendMessage() {
        const messageText = this.inputElement.value.trim();
        
        if (!messageText) return;
        if (!this.currentReceiverId) {
            showInfo('Please select a recipient first.');
            return;
        }

        // Clear input
        this.inputElement.value = '';

        try {
            // Show temporary message
            const tempMessageId = this.addTemporaryMessage(messageText, 'outgoing');
            
            // Send message via API
            const response = await sendChatMessage({
                receiver_id: this.currentReceiverId,
                message: messageText
            });

            // Update temporary message with actual data
            this.updateTemporaryMessage(tempMessageId, response.message);

            // Show success toast
            showSuccess('Message sent successfully!');

            // Clear typing indicator after sending
            this.clearTypingIndicator();
        } catch (error) {
            console.error('Error sending message:', error);
            showError('Failed to send message. Please try again.');
        }
    }

    // Add temporary message to UI
    addTemporaryMessage(text, direction) {
        const tempId = `temp-${Date.now()}`;
        const messageElement = document.createElement('div');
        messageElement.className = `message message-${direction === 'outgoing' ? 'sent' : 'received'}`;
        messageElement.id = tempId;
        messageElement.innerHTML = `
            <div>${text}</div>
            <div style="font-size: 0.75rem; opacity: 0.7; margin-top: var(--spacing-xs);">
                Sending...
            </div>
        `;
        
        this.messageContainer.appendChild(messageElement);
        this.scrollToBottom();
        
        return tempId;
    }

    // Update temporary message with actual data
    updateTemporaryMessage(tempId, actualMessage) {
        const tempElement = document.getElementById(tempId);
        if (tempElement) {
            tempElement.innerHTML = `
                <div>${actualMessage.message}</div>
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: var(--spacing-xs);">
                    ${new Date(actualMessage.timestamp).toLocaleTimeString()}
                </div>
            `;
            tempElement.id = `msg-${actualMessage.id}`;
        }
    }

    // Render messages in the chat container
    renderMessages(messages) {
        this.messageContainer.innerHTML = '';

        if (!messages || messages.length === 0) {
            this.messageContainer.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No messages yet.</p>';
            return;
        }

        messages.forEach(message => {
            const isOwnMessage = message.sender_id == this.currentUserId;
            const messageElement = this.createMessageElement(message, isOwnMessage);
            this.messageContainer.appendChild(messageElement);
        });

        this.scrollToBottom();
    }

    // Create a message element
    createMessageElement(message, isOwnMessage) {
        const messageElement = document.createElement('div');
        messageElement.className = `message message-${isOwnMessage ? 'sent' : 'received'} message-bubble-enter`;
        messageElement.innerHTML = `
            <div>${this.escapeHtml(message.message)}</div>
            <div style="font-size: 0.75rem; opacity: 0.7; margin-top: var(--spacing-xs);">
                ${new Date(message.timestamp).toLocaleTimeString()}
            </div>
        `;
        
        return messageElement;
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Scroll to bottom of chat
    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }

    // Send typing indicator
    sendTypingIndicator() {
        if (!this.currentReceiverId) return;

        // Clear previous timeout
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }

        // Send typing indicator
        sendTypingIndicator({
            receiver_id: this.currentReceiverId,
            is_typing: true
        }).catch(error => {
            console.error('Error sending typing indicator:', error);
        });

        // Set timeout to clear typing indicator after 2 seconds of inactivity
        this.typingTimeout = setTimeout(() => {
            this.clearTypingIndicator();
        }, 2000);
    }

    // Clear typing indicator
    clearTypingIndicator() {
        if (!this.currentReceiverId) return;

        sendTypingIndicator({
            receiver_id: this.currentReceiverId,
            is_typing: false
        }).catch(error => {
            console.error('Error clearing typing indicator:', error);
        });
    }

    // Open chat panel
    openChat(receiverId, receiverName = 'User') {
        this.setCurrentReceiverId(receiverId);
        document.getElementById('chatPanel').style.display = 'flex';
        document.getElementById('chatPatientName').textContent = `Chat with ${receiverName}`;
        
        // Load existing messages
        this.loadMessages();
        
        // Start polling for new messages
        this.startPolling();
    }

    // Close chat panel
    closeChat() {
        document.getElementById('chatPanel').style.display = 'none';
        this.stopPolling();
        this.clearTypingIndicator();
    }

    // Load messages for current conversation
    async loadMessages() {
        if (!this.currentReceiverId) return;

        try {
            const messages = await getChatMessages(this.currentReceiverId);
            this.renderMessages(messages);
        } catch (error) {
            console.error('Error loading messages:', error);
            showError('Failed to load messages. Please try again.');
        }
    }

    // Start polling for new messages
    startPolling() {
        this.stopPolling(); // Clear any existing polling
        
        const poll = async () => {
            if (!this.currentReceiverId) return;
            
            try {
                const messages = await getChatMessages(this.currentReceiverId);
                this.renderMessages(messages);
            } catch (error) {
                console.error('Error polling messages:', error);
                // Don't show error toasts frequently during polling
            }
        };

        // Poll every 3 seconds
        this.pollingInterval = setInterval(poll, 3000);
    }

    // Stop polling for new messages
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }
}

// Global chat UI instance
let chatUI = null;

// Initialize chat UI when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    chatUI = new ChatUI();
    chatUI.initialize();
});

// Convenience functions
const openChat = (receiverId, receiverName) => {
    if (chatUI) {
        chatUI.openChat(receiverId, receiverName);
    }
};

const closeChat = () => {
    if (chatUI) {
        chatUI.closeChat();
    }
};

const sendMessage = () => {
    if (chatUI) {
        chatUI.sendMessage();
    }
};

const loadChatMessages = async () => {
    if (chatUI) {
        await chatUI.loadMessages();
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ChatUI,
        chatUI,
        openChat,
        closeChat,
        sendMessage,
        loadChatMessages
    };
}