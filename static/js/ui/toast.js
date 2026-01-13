// Toast notification system
class ToastManager {
    constructor(containerId = 'toastContainer') {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Toast container with id '${containerId}' not found`);
            return;
        }
        this.toasts = [];
    }

    // Show a toast notification
    show(message, type = 'info', duration = 5000) {
        const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const toastElement = document.createElement('div');
        toastElement.className = `toast toast-${type}`;
        toastElement.id = toastId;
        toastElement.innerHTML = `
            <span>${message}</span>
            <button class="toast-close">&times;</button>
        `;

        // Add close functionality
        const closeButton = toastElement.querySelector('.toast-close');
        closeButton.onclick = () => this.remove(toastId);

        // Add to container
        this.container.appendChild(toastElement);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toastId);
            }, duration);
        }

        // Store toast reference
        this.toasts.push(toastId);

        return toastId;
    }

    // Remove a specific toast
    remove(toastId) {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            toastElement.classList.add('fade-out');
            setTimeout(() => {
                if (toastElement.parentNode) {
                    toastElement.parentNode.removeChild(toastElement);
                }
                this.toasts = this.toasts.filter(id => id !== toastId);
            }, 300);
        }
    }

    // Show success toast
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    // Show error toast
    error(message, duration = 7000) {
        return this.show(message, 'error', duration);
    }

    // Show info toast
    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    // Show warning toast
    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    // Clear all toasts
    clear() {
        this.toasts.forEach(toastId => this.remove(toastId));
        this.toasts = [];
    }
}

// Global toast manager instance
let toastManager = null;

// Initialize toast manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    toastManager = new ToastManager();
});

// Convenience functions
const showToast = (message, type = 'info', duration) => {
    if (toastManager) {
        return toastManager.show(message, type, duration);
    } else {
        console.warn('Toast manager not initialized yet');
        // Fallback to alert for now
        alert(message);
    }
};

const showSuccess = (message, duration) => showToast(message, 'success', duration);
const showError = (message, duration) => showToast(message, 'error', duration);
const showInfo = (message, duration) => showToast(message, 'info', duration);
const showWarning = (message, duration) => showToast(message, 'warning', duration);

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ToastManager,
        toastManager,
        showToast,
        showSuccess,
        showError,
        showInfo,
        showWarning
    };
}