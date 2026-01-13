// Authentication management
class AuthManager {
    constructor() {
        this.token = localStorage.getItem('token');
        this.user = JSON.parse(localStorage.getItem('user')) || null;
    }

    // Store authentication data
    setAuthData(token, userData) {
        this.token = token;
        this.user = userData;
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(userData));
    }

    // Clear authentication data
    clearAuthData() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get current user role
    getUserRole() {
        return this.user?.role || null;
    }

    // Get current user ID
    getUserId() {
        return this.user?.id || null;
    }

    // Get current username
    getUsername() {
        return this.user?.username || null;
    }

    // Logout user
    async logout() {
        try {
            await logout();
            this.clearAuthData();
            window.location.href = '/login';
        } catch (error) {
            console.error('Logout error:', error);
            this.clearAuthData();
            window.location.href = '/login';
        }
    }
}

// Global auth manager instance
const authManager = new AuthManager();

// Convenience functions
const isAuthenticated = () => authManager.isAuthenticated();
const getUserRole = () => authManager.getUserRole();
const getUserId = () => authManager.getUserId();
const getUsername = () => authManager.getUsername();
const logoutUser = () => authManager.logout();

// Set up global event listeners for auth
document.addEventListener('DOMContentLoaded', function() {
    // Add logout functionality to any element with onclick="logout()"
    if (typeof logout === 'undefined') {
        window.logout = async function() {
            await logoutUser();
        };
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AuthManager,
        authManager,
        isAuthenticated,
        getUserRole,
        getUserId,
        getUsername,
        logoutUser
    };
}