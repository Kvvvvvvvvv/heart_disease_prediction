// Chat API functions
class ChatApi {
    constructor() {
        this.apiClient = new ApiClient();
        this.pollingInterval = null;
    }

    // Send a message
    async sendMessage(messageData) {
        return this.apiClient.sendMessage(messageData);
    }

    // Get messages with a specific user
    async getMessages(receiverId) {
        return this.apiClient.getMessages(receiverId);
    }

    // Get all conversations for the current user
    async getConversations() {
        return this.apiClient.getConversations();
    }

    // Send typing indicator
    async sendTypingIndicator(typingData) {
        return this.apiClient.sendTypingIndicator(typingData);
    }

    // Mark message as delivered
    async markMessageDelivered(messageId) {
        return this.apiClient.markMessageDelivered(messageId);
    }

    // Get chat logs (admin only)
    async getChatLogs() {
        return this.apiClient.getChatLogs();
    }

    // Start polling for new messages
    startPolling(receiverId, callback, interval = 3000) {
        this.stopPolling();
        this.pollingInterval = setInterval(async () => {
            try {
                const messages = await this.getMessages(receiverId);
                callback(messages);
            } catch (error) {
                console.error('Error polling messages:', error);
            }
        }, interval);
    }

    // Stop polling for new messages
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }
}

// Global chat API instance
const chatApi = new ChatApi();

// Convenience functions
const sendChatMessage = (messageData) => chatApi.sendMessage(messageData);
const getChatMessages = (receiverId) => chatApi.getMessages(receiverId);
const getChatConversations = () => chatApi.getConversations();
const sendTypingIndicator = (typingData) => chatApi.sendTypingIndicator(typingData);
const markChatMessageDelivered = (messageId) => chatApi.markMessageDelivered(messageId);
const getChatLogs = () => chatApi.getChatLogs();
const startChatPolling = (receiverId, callback, interval) => chatApi.startPolling(receiverId, callback, interval);
const stopChatPolling = () => chatApi.stopPolling();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ChatApi,
        chatApi,
        sendChatMessage,
        getChatMessages,
        getChatConversations,
        sendTypingIndicator,
        markChatMessageDelivered,
        getChatLogs,
        startChatPolling,
        stopChatPolling
    };
}