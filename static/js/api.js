// API Wrapper for fetching data with proper error handling
class ApiClient {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
    }

    // Generic fetch wrapper with error handling
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',  // Include cookies with requests
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            // Check if response is ok before attempting to parse JSON
            if (!response.ok) {
                // Try to get error text if available
                let errorData;
                try {
                    errorData = await response.text();
                    // Attempt to parse as JSON if possible
                    try {
                        errorData = JSON.parse(errorData);
                    } catch {
                        // If not JSON, use as string
                    }
                } catch {
                    errorData = `HTTP error! status: ${response.status}`;
                }
                
                const errorMessage = typeof errorData === 'object' && errorData.message 
                    ? errorData.message 
                    : (typeof errorData === 'string' ? errorData : `HTTP error! status: ${response.status}`);
                
                throw new Error(errorMessage);
            }
            
            // Safely parse the JSON response
            const data = await response.json();
            
            // Validate that the response follows the expected format
            if (data.status !== 'success' && data.status !== 'error') {
                throw new Error('Invalid API response format: missing status field');
            }
            
            if (data.status === 'error') {
                throw new Error(data.message || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication methods
    async login(credentials) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    async logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    }

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async getProfile() {
        return this.request('/auth/profile', {
            method: 'GET'
        });
    }

    // User methods
    async getUserDashboard() {
        return this.request('/user/dashboard', {
            method: 'GET'
        });
    }

    async makePrediction(patientData) {
        return this.request('/user/predict', {
            method: 'POST',
            body: JSON.stringify(patientData)
        });
    }

    async getPredictionHistory() {
        return this.request('/user/predictions/history', {
            method: 'GET'
        });
    }

    async requestConsultation() {
        return this.request('/user/request_consultation', {
            method: 'POST'
        });
    }

    async getAssignedDoctor() {
        return this.request('/user/assigned_doctor', {
            method: 'GET'
        });
    }

    // Doctor methods
    async getDoctorDashboard() {
        return this.request('/doctor/dashboard', {
            method: 'GET'
        });
    }

    async getAssignedUsers() {
        return this.request('/doctor/users', {
            method: 'GET'
        });
    }

    async getUserPredictions(userId) {
        return this.request(`/doctor/user/${userId}/predictions`, {
            method: 'GET'
        });
    }

    async updateConsultationStatus(data) {
        return this.request('/doctor/consultation/update_status', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async searchPatients(query) {
        const params = query ? `?q=${encodeURIComponent(query)}` : '';
        return this.request(`/doctor/patients/search${params}`, {
            method: 'GET'
        });
    }

    // Admin methods
    async getAdminDashboard() {
        return this.request('/admin/dashboard', {
            method: 'GET'
        });
    }

    async getAllUsers() {
        return this.request('/admin/users', {
            method: 'GET'
        });
    }

    async getAllDoctors() {
        return this.request('/admin/doctors', {
            method: 'GET'
        });
    }

    async createUser(userData) {
        return this.request('/admin/users', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async updateUser(userId, userData) {
        return this.request(`/admin/users/${userId}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }

    async deleteUser(userId) {
        return this.request(`/admin/users/${userId}`, {
            method: 'DELETE'
        });
    }

    async assignUserToDoctor(assignmentData) {
        return this.request('/admin/assignments', {
            method: 'POST',
            body: JSON.stringify(assignmentData)
        });
    }

    async getSystemLogs() {
        return this.request('/admin/logs', {
            method: 'GET'
        });
    }

    // Chat methods
    async sendMessage(messageData) {
        return this.request('/chat/send', {
            method: 'POST',
            body: JSON.stringify(messageData)
        });
    }

    async getMessages(receiverId) {
        return this.request(`/chat/messages/${receiverId}`, {
            method: 'GET'
        });
    }

    async getConversations() {
        return this.request('/chat/conversations', {
            method: 'GET'
        });
    }

    async sendTypingIndicator(typingData) {
        return this.request('/chat/typing', {
            method: 'POST',
            body: JSON.stringify(typingData)
        });
    }

    async markMessageDelivered(messageId) {
        return this.request(`/chat/mark_delivered/${messageId}`, {
            method: 'POST'
        });
    }

    async getChatLogs() {
        return this.request('/chat/admin/logs', {
            method: 'GET'
        });
    }
}

// Global API client instance
const apiClient = new ApiClient();

// Convenience functions for direct use
const login = (credentials) => apiClient.login(credentials);
const logout = () => apiClient.logout();
const register = (userData) => apiClient.register(userData);
const getProfile = () => apiClient.getProfile();

const getUserDashboard = () => apiClient.getUserDashboard();
const makePrediction = (patientData) => apiClient.makePrediction(patientData);
const getPredictionHistory = () => apiClient.getPredictionHistory();
const requestConsultation = () => apiClient.requestConsultation();
const getAssignedDoctor = () => apiClient.getAssignedDoctor();

const getDoctorDashboard = () => apiClient.getDoctorDashboard();
const getAssignedUsers = () => apiClient.getAssignedUsers();
const getUserPredictions = (userId) => apiClient.getUserPredictions(userId);
const updateConsultationStatus = (data) => apiClient.updateConsultationStatus(data);
const searchPatients = (query) => apiClient.searchPatients(query);

const getAdminDashboard = () => apiClient.getAdminDashboard();
const getAllUsers = () => apiClient.getAllUsers();
const getAllDoctors = () => apiClient.getAllDoctors();
const createUser = (userData) => apiClient.createUser(userData);
const updateUser = (userId, userData) => apiClient.updateUser(userId, userData);
const deleteUser = (userId) => apiClient.deleteUser(userId);
const assignUserToDoctor = (assignmentData) => apiClient.assignUserToDoctor(assignmentData);
const getSystemLogs = () => apiClient.getSystemLogs();

const sendMessage = (messageData) => apiClient.sendMessage(messageData);
const getMessages = (receiverId) => apiClient.getMessages(receiverId);
const getConversations = () => apiClient.getConversations();
const sendTypingIndicator = (typingData) => apiClient.sendTypingIndicator(typingData);
const markMessageDelivered = (messageId) => apiClient.markMessageDelivered(messageId);
const getChatLogs = () => apiClient.getChatLogs();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ApiClient,
        apiClient,
        login, logout, register, getProfile,
        getUserDashboard, makePrediction, getPredictionHistory, requestConsultation, getAssignedDoctor,
        getDoctorDashboard, getAssignedUsers, getUserPredictions, updateConsultationStatus, searchPatients,
        getAdminDashboard, getAllUsers, getAllDoctors, createUser, updateUser, deleteUser, assignUserToDoctor, getSystemLogs,
        sendMessage, getMessages, getConversations, sendTypingIndicator, markMessageDelivered, getChatLogs
    };
}