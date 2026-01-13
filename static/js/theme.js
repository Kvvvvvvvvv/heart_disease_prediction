// Theme management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.setupEventListeners();
    }

    // Apply theme to document
    applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
    }

    // Toggle between light and dark theme
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        return newTheme;
    }

    // Set specific theme
    setTheme(theme) {
        this.applyTheme(theme);
    }

    // Get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Setup event listeners
    setupEventListeners() {
        const themeToggleBtn = document.getElementById('themeToggle');
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', () => {
                const newTheme = this.toggleTheme();
                themeToggleBtn.textContent = newTheme === 'dark' ? '☀️' : '🌙';
            });
        }
    }
}

// Global theme manager instance
const themeManager = new ThemeManager();

// Convenience functions
const toggleTheme = () => themeManager.toggleTheme();
const setTheme = (theme) => themeManager.setTheme(theme);
const getCurrentTheme = () => themeManager.getCurrentTheme();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThemeManager,
        themeManager,
        toggleTheme,
        setTheme,
        getCurrentTheme
    };
}