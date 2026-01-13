// User dashboard functionality
class UserDashboard {
    constructor() {
        this.currentTab = 'dashboard';
        this.userData = null;
        this.assignedDoctor = null;
        this.chatReceiverId = null;
        this.chatInterval = null;
    }

    // Initialize the dashboard
    async initialize() {
        try {
            // Load user data
            const userDashboardResponse = await getUserDashboard();
            this.userData = userDashboardResponse.data;
            
            const assignedDoctorResponse = await getAssignedDoctor();
            this.assignedDoctor = assignedDoctorResponse.data || assignedDoctorResponse;
            
            // Update UI with user data
            this.updateUserInfo();
            this.updateDashboardStats();
            this.updateAssignedDoctor();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Load prediction history
            await this.loadPredictionHistory();
            
            console.log('User dashboard initialized successfully');
        } catch (error) {
            console.error('Error initializing user dashboard:', error);
            showError('Failed to initialize dashboard. Please try refreshing the page.');
        }
    }

    // Update user info in header
    updateUserInfo() {
        if (this.userData?.user?.username) {
            document.getElementById('userName').textContent = this.userData.user.username;
        }
    }

    // Update dashboard statistics
    updateDashboardStats() {
        if (!this.userData) return;

        // Calculate statistics
        const totalPredictions = this.userData.predictions.length;
        const highRiskCount = this.userData.predictions.filter(p => p.prediction_result === 1).length;
        const avgConfidence = this.userData.predictions.length > 0 
            ? (this.userData.predictions.reduce((sum, p) => sum + (p.confidence_score || 0), 0) / this.userData.predictions.length * 100).toFixed(1)
            : 0;

        // Update stat elements
        document.getElementById('totalPredictions').textContent = totalPredictions;
        document.getElementById('highRiskCount').textContent = highRiskCount;
        document.getElementById('avgConfidence').textContent = `${avgConfidence}%`;

        // Update last consultation date
        const lastConsultationEl = document.getElementById('lastConsultation');
        if (this.userData.predictions.length > 0) {
            const lastPrediction = this.userData.predictions[0];
            lastConsultationEl.textContent = new Date(lastPrediction.created_at).toLocaleDateString();
        } else {
            lastConsultationEl.textContent = 'Never';
        }
    }

    // Update assigned doctor section
    updateAssignedDoctor() {
        const doctorContainer = document.getElementById('assignedDoctor');
        if (this.assignedDoctor && this.assignedDoctor.username) {
            doctorContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <div style="display: flex; align-items: center; gap: var(--spacing-md);">
                            <div class="avatar">D</div>
                            <div>
                                <h4 style="margin: 0;">Dr. ${this.assignedDoctor.username}</h4>
                                <p style="margin: var(--spacing-xs) 0 0 0; color: var(--text-secondary);">Cardiologist</p>
                            </div>
                        </div>
                        <div style="margin-top: var(--spacing-md);">
                            <button class="btn btn-primary" onclick="openChat(${this.assignedDoctor.id})">
                                <span>💬</span> Chat Now
                            </button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            doctorContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <p>No doctor assigned yet. Please contact administration.</p>
                    </div>
                </div>
            `;
        }
    }

    // Set up event listeners
    setupEventListeners() {
        // Tab switching
        const tabItems = document.querySelectorAll('.nav-item[data-tab]');
        tabItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const tabName = e.currentTarget.getAttribute('data-tab');
                this.switchTab(tabName);
            });
        });

        // Sidebar toggle for mobile
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', () => {
                document.querySelector('.sidebar').classList.toggle('active');
            });
        }

        // Prediction form submission
        const predictionForm = document.getElementById('predictionForm');
        if (predictionForm) {
            predictionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handlePredictionSubmit(e);
            });
        }

        // Chat functionality
        this.setupChatFunctionality();
    }

    // Switch between tabs
    switchTab(tabName) {
        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`.nav-item[data-tab="${tabName}"]`).classList.add('active');

        // Hide all tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });

        // Show selected tab content
        document.getElementById(`${tabName}Tab`).style.display = 'block';

        // Update current tab
        this.currentTab = tabName;

        // Load content based on tab
        switch(tabName) {
            case 'history':
                this.loadPredictionHistory();
                break;
            case 'chat':
                this.loadChatContent();
                break;
            case 'profile':
                this.loadProfileContent();
                break;
        }
    }

    // Handle prediction form submission
    async handlePredictionSubmit(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const resultContainer = document.getElementById('predictionResults');

        try {
            // Show loading state
            showSpinnerInButton(submitBtn);
            resultContainer.style.display = 'none';

            // Get form data
            const formData = new FormData(form);
            const patientData = Object.fromEntries(formData.entries());

            // Convert numeric values
            patientData.age = parseInt(patientData.age);
            patientData.sex = parseInt(patientData.sex);
            patientData.cp = parseInt(patientData.cp);
            patientData.trestbps = parseInt(patientData.trestbps);
            patientData.chol = parseInt(patientData.chol);
            patientData.fbs = parseInt(patientData.fbs);
            patientData.restecg = parseInt(patientData.restecg);
            patientData.thalach = parseInt(patientData.thalach);
            patientData.exang = parseInt(patientData.exang);
            patientData.oldpeak = parseFloat(patientData.oldpeak);
            patientData.slope = parseInt(patientData.slope);
            patientData.ca = parseInt(patientData.ca);
            patientData.thal = parseInt(patientData.thal);

            // Make prediction
            const resultResponse = await makePrediction(patientData);
            const result = resultResponse.data;

            // Display results
            this.displayPredictionResult(result);
            resultContainer.style.display = 'block';

            // Show success toast
            showSuccess('Prediction completed successfully!');

            // Reload dashboard stats
            this.userData = await getUserDashboard();
            this.updateDashboardStats();

        } catch (error) {
            console.error('Prediction error:', error);
            showError('Failed to make prediction. Please try again.');
        } finally {
            // Restore button
            restoreButton(submitBtn);
        }
    }

    // Display prediction result
    displayPredictionResult(result) {
        const resultContainer = document.getElementById('predictionResults');
        
        let riskClass = '';
        let riskText = '';
        let icon = '';
        
        if (result.risk_level === 'High') {
            riskClass = 'result-high-risk';
            riskText = 'High Risk';
            icon = '🚨';
        } else if (result.risk_level === 'Medium') {
            riskClass = 'result-medium-risk';
            riskText = 'Medium Risk';
            icon = '⚠️';
        } else {
            riskClass = 'result-low-risk';
            riskText = 'Low Risk';
            icon = '✅';
        }

        resultContainer.className = `results-container ${riskClass}`;
        resultContainer.innerHTML = `
            <div class="result-header">
                <div class="result-icon">${icon}</div>
                <div>
                    <h3 class="result-title">${riskText} - Heart Disease Prediction</h3>
                    <p class="result-subtitle">Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                </div>
            </div>
            
            <div style="margin: var(--spacing-lg) 0;">
                <p><strong>Prediction:</strong> ${result.prediction === 1 ? 'Positive - High probability of heart disease' : 'Negative - Low probability of heart disease'}</p>
                <p><strong>Risk Level:</strong> ${result.risk_level}</p>
                <p><strong>Probability Distribution:</strong></p>
                <ul>
                    <li>No Disease: ${(result.probabilities.no_disease * 100).toFixed(1)}%</li>
                    <li>Has Disease: ${(result.probabilities.has_disease * 100).toFixed(1)}%</li>
                </ul>
            </div>
            
            <div style="margin: var(--spacing-lg) 0;">
                <h4 style="margin-bottom: var(--spacing-md);">Recommendations:</h4>
                <div id="recommendations">
                    ${this.generateRecommendations(result)}
                </div>
            </div>
            
            <div style="margin: var(--spacing-lg) 0;">
                <div class="confidence-meter">
                    <div class="confidence-fill" style="width: ${(result.confidence * 100)}%;"></div>
                </div>
                <p style="text-align: center; margin-top: var(--spacing-sm); color: var(--text-secondary);">
                    Model Confidence: ${(result.confidence * 100).toFixed(1)}%
                </p>
            </div>
            
            <div style="margin-top: var(--spacing-lg);">
                <button class="btn btn-primary" onclick="requestConsultationWrapper()">
                    <span>👨‍⚕️</span> Request Doctor Consultation
                </button>
            </div>
        `;
    }

    // Generate recommendations based on result
    generateRecommendations(result) {
        let recommendations = '<ul>';
        
        if (result.risk_level === 'High') {
            recommendations += `
                <li style="color: var(--danger);">Consult with a cardiologist immediately</li>
                <li>Schedule diagnostic tests (ECG, echocardiogram, stress test)</li>
                <li>Consider lifestyle changes and medication</li>
                <li>Monitor blood pressure and cholesterol regularly</li>
            `;
        } else if (result.risk_level === 'Medium') {
            recommendations += `
                <li>Schedule a follow-up with your primary care physician</li>
                <li>Consider additional screening tests</li>
                <li>Focus on preventive measures</li>
                <li>Maintain healthy lifestyle habits</li>
            `;
        } else {
            recommendations += `
                <li>Maintain your current healthy habits</li>
                <li>Continue regular health screenings</li>
                <li>Stay physically active</li>
                <li>Follow a balanced diet</li>
            `;
        }
        
        recommendations += '</ul>';
        return recommendations;
    }

    // Load prediction history
    async loadPredictionHistory() {
        try {
            const historyContainer = document.getElementById('historyContent');
            showSkeletonText(historyContainer, 5);

            const historyResponse = await getPredictionHistory();
                        const predictions = historyResponse.data;
            
            if (predictions.length === 0) {
                historyContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No prediction history available. Make your first prediction in the Prediction tab.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let historyHtml = `
                <div class="card">
                    <div class="card-body">
                        <table class="history-table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Prediction</th>
                                    <th>Confidence</th>
                                    <th>Risk Level</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            predictions.forEach(prediction => {
                const date = new Date(prediction.created_at).toLocaleDateString();
                const predictionText = prediction.prediction_result === 1 ? 'High Risk' : 'Low Risk';
                const riskLevel = this.getRiskLevelFromConfidence(prediction.confidence_score);
                
                historyHtml += `
                    <tr>
                        <td>${date}</td>
                        <td>${predictionText}</td>
                        <td>${(prediction.confidence_score * 100).toFixed(1)}%</td>
                        <td><span class="badge badge-${riskLevel.toLowerCase()}">${riskLevel}</span></td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="showPredictionDetails(${prediction.id})">
                                View Details
                            </button>
                        </td>
                    </tr>
                `;
            });

            historyHtml += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            historyContainer.innerHTML = historyHtml;

        } catch (error) {
            console.error('Error loading prediction history:', error);
            showError('Failed to load prediction history.');
        }
    }

    // Get risk level from confidence score
    getRiskLevelFromConfidence(confidence) {
        if (confidence >= 0.7) return 'High';
        if (confidence >= 0.4) return 'Medium';
        return 'Low';
    }

    // Setup chat functionality
    setupChatFunctionality() {
        // Chat panel toggle
        window.openChat = (receiverId) => {
            this.chatReceiverId = receiverId;
            document.getElementById('chatPanel').style.display = 'flex';
            this.loadChatMessages();
            
            // Start polling for new messages
            this.startChatPolling();
        };

        window.closeChat = () => {
            document.getElementById('chatPanel').style.display = 'none';
            this.stopChatPolling();
        };

        window.sendMessage = async () => {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (!message) return;
            if (!this.chatReceiverId) {
                showError('No recipient selected for chat.');
                return;
            }

            try {
                const response = await sendMessage({
                    receiver_id: this.chatReceiverId,
                    message: message
                });
                console.log('Message sent:', response);

                input.value = '';
                await this.loadChatMessages(); // Refresh messages
            } catch (error) {
                console.error('Error sending message:', error);
                showError('Failed to send message. Please try again.');
            }
        };

        // Allow sending message with Enter key
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Start chat polling
    startChatPolling() {
        this.stopChatPolling(); // Clear any existing interval
        this.chatInterval = setInterval(async () => {
            await this.loadChatMessages();
        }, 3000); // Poll every 3 seconds
    }

    // Stop chat polling
    stopChatPolling() {
        if (this.chatInterval) {
            clearInterval(this.chatInterval);
            this.chatInterval = null;
        }
    }

    // Load chat messages
    async loadChatMessages() {
        if (!this.chatReceiverId) return;

        try {
            const messagesResponse = await getMessages(this.chatReceiverId);
            const messages = messagesResponse.data.messages;
            const messagesContainer = document.getElementById('chatMessages');
            
            messagesContainer.innerHTML = '';

            messages.forEach(message => {
                const isOwnMessage = message.sender_id == getUserId(); // Using auth manager to get user ID
                const messageClass = isOwnMessage ? 'message-sent' : 'message-received';
                
                const messageElement = document.createElement('div');
                messageElement.className = `message ${messageClass}`;
                messageElement.innerHTML = `
                    <div>${message.message}</div>
                    <div style="font-size: 0.75rem; opacity: 0.7; margin-top: var(--spacing-xs);">
                        ${new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                `;
                
                messagesContainer.appendChild(messageElement);
            });

            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } catch (error) {
            console.error('Error loading chat messages:', error);
        }
    }

    // Load chat content for chat tab
    loadChatContent() {
        // Content is handled by the chat panel functionality
        // Just ensure the chat panel is available
    }

    // Load profile content
    async loadProfileContent() {
        const profileContainer = document.getElementById('profileContent');
        
        if (this.userData?.user) {
            profileContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <div style="display: flex; align-items: center; gap: var(--spacing-md); margin-bottom: var(--spacing-lg);">
                            <div class="avatar">${this.userData.user.username.charAt(0).toUpperCase()}</div>
                            <div>
                                <h3>${this.userData.user.username}</h3>
                                <p style="margin: var(--spacing-xs) 0 0 0; color: var(--text-secondary);">User ID: ${this.userData.user.id}</p>
                            </div>
                        </div>
                        
                        <div style="margin-top: var(--spacing-lg);">
                            <h4>Account Information</h4>
                            <p><strong>Email:</strong> ${this.userData.user.email || 'Not provided'}</p>
                            <p><strong>Member Since:</strong> ${new Date(this.userData.user.created_at).toLocaleDateString()}</p>
                            <p><strong>Total Predictions:</strong> ${this.userData.predictions.length}</p>
                        </div>
                        
                        <div style="margin-top: var(--spacing-lg);">
                            <button class="btn btn-secondary" onclick="changePassword()">
                                Change Password
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }
    }
}

// Global function wrappers for inline event handlers
window.requestConsultationWrapper = async () => {
    try {
        await requestConsultation();
        showSuccess('Consultation request sent to your assigned doctor!');
    } catch (error) {
        console.error('Error requesting consultation:', error);
        showError('Failed to send consultation request. Please try again.');
    }
};

window.showPredictionDetails = (predictionId) => {
    // In a real app, this would show detailed prediction information
    alert(`Detailed information for prediction ID: ${predictionId}`);
};

window.changePassword = () => {
    // In a real app, this would open a password change modal
    alert('Password change functionality would open here');
};

// Global user dashboard instance
let userDashboard = null;

// Initialize user dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    userDashboard = new UserDashboard();
    await userDashboard.initialize();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        UserDashboard,
        userDashboard
    };
}