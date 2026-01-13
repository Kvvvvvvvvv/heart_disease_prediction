// Loader utility functions
class LoaderManager {
    constructor() {
        this.loaders = new Map();
    }

    // Show loader on a specific element
    showLoader(element, type = 'overlay') {
        const elementId = this.getElementId(element);
        
        if (this.loaders.has(elementId)) {
            this.hideLoader(element);
        }

        if (type === 'overlay') {
            this.showOverlayLoader(element);
        } else if (type === 'spinner') {
            this.showSpinnerLoader(element);
        } else if (type === 'skeleton') {
            this.showSkeletonLoader(element);
        }
    }

    // Hide loader from a specific element
    hideLoader(element) {
        const elementId = this.getElementId(element);
        const loaderData = this.loaders.get(elementId);
        
        if (loaderData) {
            loaderData.loader.remove();
            this.loaders.delete(elementId);
        }
    }

    // Show overlay loader
    showOverlayLoader(element) {
        const loader = document.createElement('div');
        loader.className = 'loading-overlay';
        loader.innerHTML = '<div class="spinner"></div>';
        loader.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 0.5rem;
            align-items: center;
            justify-content: center;
            z-index: 10;
            display: flex;
        `;

        // Position relative to the element
        const rect = element.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(element);
        
        if (computedStyle.position === 'static') {
            element.style.position = 'relative';
        }

        element.appendChild(loader);
        element.style.overflow = 'hidden';

        this.loaders.set(this.getElementId(element), {
            loader,
            originalOverflow: element.style.overflow
        });
    }

    // Show spinner loader inside a button
    showSpinnerInButton(buttonElement) {
        const originalHTML = buttonElement.innerHTML;
        const originalDisabled = buttonElement.disabled;
        
        buttonElement.innerHTML = '<span class="spinner"></span>';
        buttonElement.disabled = true;
        
        this.loaders.set(this.getElementId(buttonElement), {
            originalHTML,
            originalDisabled
        });
    }

    // Restore button to original state
    restoreButton(buttonElement) {
        const loaderData = this.loaders.get(this.getElementId(buttonElement));
        
        if (loaderData) {
            buttonElement.innerHTML = loaderData.originalHTML;
            buttonElement.disabled = loaderData.originalDisabled;
            this.loaders.delete(this.getElementId(buttonElement));
        }
    }

    // Show skeleton loader
    showSkeletonLoader(element) {
        const originalHTML = element.innerHTML;
        element.innerHTML = '';
        
        // Create skeleton elements based on the expected content structure
        const skeletonDiv = document.createElement('div');
        skeletonDiv.className = 'skeleton';
        skeletonDiv.style.height = '100px';
        skeletonDiv.style.marginBottom = 'var(--spacing-md)';
        
        element.appendChild(skeletonDiv);
        
        this.loaders.set(this.getElementId(element), {
            originalHTML
        });
    }

    // Show skeleton text lines
    showSkeletonText(parentElement, lines = 3) {
        const originalHTML = parentElement.innerHTML;
        parentElement.innerHTML = '';
        
        for (let i = 0; i < lines; i++) {
            const skeletonLine = document.createElement('div');
            skeletonLine.className = 'skeleton skeleton-text-line';
            skeletonLine.style.width = `${70 + Math.random() * 30}%`;
            if (i < lines - 1) {
                skeletonLine.style.marginBottom = 'var(--spacing-xs)';
            }
            parentElement.appendChild(skeletonLine);
        }
        
        this.loaders.set(this.getElementId(parentElement), {
            originalHTML
        });
    }

    // Restore skeleton loader to original content
    restoreSkeleton(element) {
        const loaderData = this.loaders.get(this.getElementId(element));
        
        if (loaderData) {
            element.innerHTML = loaderData.originalHTML;
            this.loaders.delete(this.getElementId(element));
        }
    }

    // Get unique ID for an element
    getElementId(element) {
        if (!element.__loaderId) {
            element.__loaderId = `loader-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        }
        return element.__loaderId;
    }

    // Check if element has loader
    hasLoader(element) {
        return this.loaders.has(this.getElementId(element));
    }
}

// Global loader manager instance
const loaderManager = new LoaderManager();

// Convenience functions
const showLoader = (element, type = 'overlay') => loaderManager.showLoader(element, type);
const hideLoader = (element) => loaderManager.hideLoader(element);
const showSpinnerInButton = (button) => loaderManager.showSpinnerInButton(button);
const restoreButton = (button) => loaderManager.restoreButton(button);
const showSkeletonLoader = (element) => loaderManager.showSkeletonLoader(element);
const showSkeletonText = (parent, lines) => loaderManager.showSkeletonText(parent, lines);
const restoreSkeleton = (element) => loaderManager.restoreSkeleton(element);
const hasLoader = (element) => loaderManager.hasLoader(element);

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        LoaderManager,
        loaderManager,
        showLoader,
        hideLoader,
        showSpinnerInButton,
        restoreButton,
        showSkeletonLoader,
        showSkeletonText,
        restoreSkeleton,
        hasLoader
    };
}