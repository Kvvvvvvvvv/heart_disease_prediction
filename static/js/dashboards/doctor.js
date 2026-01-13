// Doctor dashboard functionality
class DoctorDashboard {
    constructor() {
        this.currentTab = 'dashboard';
        this.doctorData = null;
        this.chatReceiverId = null;
        this.chatInterval = null;
    }

    // Initialize the dashboard
    async initialize() {
        try {
            // Load doctor data
            const doctorDashboardResponse = await getDoctorDashboard();
            this.doctorData = doctorDashboardResponse.data;
            
            // Update UI with doctor data
            this.updateUserInfo();
            this.updateDashboardStats();
            this.updateRecentConsultations();
            this.updateCriticalCases();
            
            // Set up event listeners
            this.setupEventListeners();
            
            console.log('Doctor dashboard initialized successfully');
        } catch (error) {
            console.error('Error initializing doctor dashboard:', error);
            showError('Failed to initialize dashboard. Please try refreshing the page.');
        }
    }

    // Update user info in header
    updateUserInfo() {
        if (this.doctorData?.doctor?.username) {
            document.getElementById('userName').textContent = this.doctorData.doctor.username;
        }
    }

    // Update dashboard statistics
    updateDashboardStats() {
        if (!this.doctorData) return;

        // Calculate statistics
        const totalPatients = this.doctorData.assigned_users.length;
        const activeConsultations = this.doctorData.consultations.length;
        const highRiskCases = this.doctorData.consultations.filter(c => c.prediction_result === 1).length;

        // Update stat elements
        document.getElementById('totalPatients').textContent = totalPatients;
        document.getElementById('activeConsultations').textContent = activeConsultations;
        document.getElementById('highRiskCases').textContent = highRiskCases;
        document.getElementById('avgResponseTime').textContent = '--'; // Placeholder for now
    }

    // Update recent consultations
    updateRecentConsultations() {
        const consultationsContainer = document.getElementById('recentConsultations');
        if (!this.doctorData || !this.doctorData.consultations.length) {
            consultationsContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <p>No recent consultations available.</p>
                    </div>
                </div>
            `;
            return;
        }

        let consultationsHtml = '<div class="patient-list">';
        
        this.doctorData.consultations.slice(0, 5).forEach(consultation => {
            const riskLevel = consultation.prediction_result === 1 ? 'High' : 'Low';
            const riskClass = consultation.prediction_result === 1 ? 'risk-high' : 'risk-low';
            const date = new Date(consultation.created_at).toLocaleDateString();
            
            consultationsHtml += `
                <div class="patient-card">
                    <div class="patient-header">
                        <div class="patient-name">${consultation.username}</div>
                        <div class="patient-id">ID: ${consultation.user_id}</div>
                    </div>
                    <div class="patient-info">
                        <div class="info-item">
                            <span class="info-label">Risk Level</span>
                            <span class="info-value ${riskClass}">${riskLevel} Risk</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Confidence</span>
                            <span class="info-value">${(consultation.confidence_score * 100).toFixed(1)}%</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Date</span>
                            <span class="info-value">${date}</span>
                        </div>
                    </div>
                    <div class="patient-actions">
                        <button class="btn btn-sm btn-outline" onclick="viewPatientDetails(${consultation.user_id})">
                            View Details
                        </button>
                        <button class="btn btn-sm btn-primary" onclick="openChatWithPatient(${consultation.user_id})">
                            Chat
                        </button>
                    </div>
                </div>
            `;
        });

        consultationsHtml += '</div>';
        consultationsContainer.innerHTML = consultationsHtml;
    }

    // Update critical cases
    updateCriticalCases() {
        const criticalCasesContainer = document.getElementById('criticalCases');
        if (!this.doctorData || !this.doctorData.consultations.length) {
            criticalCasesContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <p>No critical cases at the moment.</p>
                    </div>
                </div>
            `;
            return;
        }

        // Filter high-risk cases
        const highRiskCases = this.doctorData.consultations.filter(c => c.prediction_result === 1).slice(0, 3);

        if (highRiskCases.length === 0) {
            criticalCasesContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <p>No high-risk cases at the moment.</p>
                    </div>
                </div>
            `;
            return;
        }

        let criticalHtml = '<div class="patient-list">';
        
        highRiskCases.forEach(caseData => {
            const date = new Date(caseData.created_at).toLocaleDateString();
            
            criticalHtml += `
                <div class="patient-card" style="border-left: 4px solid var(--danger);">
                    <div class="patient-header">
                        <div class="patient-name">🚨 ${caseData.username}</div>
                        <div class="patient-id">ID: ${caseData.user_id}</div>
                    </div>
                    <div class="patient-info">
                        <div class="info-item">
                            <span class="info-label">High Risk Alert</span>
                            <span class="info-value risk-high">Immediate Attention Needed</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Confidence</span>
                            <span class="info-value">${(caseData.confidence_score * 100).toFixed(1)}%</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Date</span>
                            <span class="info-value">${date}</span>
                        </div>
                    </div>
                    <div class="patient-actions">
                        <button class="btn btn-sm btn-danger" onclick="escalateCase(${caseData.user_id})">
                            Escalate
                        </button>
                        <button class="btn btn-sm btn-primary" onclick="openChatWithPatient(${caseData.user_id})">
                            Contact Patient
                        </button>
                    </div>
                </div>
            `;
        });

        criticalHtml += '</div>';
        criticalCasesContainer.innerHTML = criticalHtml;
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

        // Patient search functionality
        const patientSearch = document.getElementById('patientSearch');
        if (patientSearch) {
            patientSearch.addEventListener('input', this.debounce((e) => {
                this.searchPatients(e.target.value);
            }, 300));
        }

        // Chat functionality
        this.setupChatFunctionality();
    }

    // Debounce function for search
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
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
            case 'patients':
                this.loadPatientsTab();
                break;
            case 'consultations':
                this.loadConsultationsTab();
                break;
            case 'chat':
                this.loadChatTab();
                break;
            case 'reports':
                this.loadReportsTab();
                break;
        }
    }

    // Load patients tab
    async loadPatientsTab() {
        try {
            const patientsContainer = document.getElementById('patientsList');
            showSkeletonText(patientsContainer, 5);

            const patients = await getAssignedUsers();
            
            if (!patients || patients.length === 0) {
                patientsContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No patients assigned to you yet.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let patientsHtml = '<div class="patient-list">';
            
            patients.forEach(patient => {
                patientsHtml += `
                    <div class="patient-card">
                        <div class="patient-header">
                            <div class="patient-name">${patient.username}</div>
                            <div class="patient-id">ID: ${patient.id}</div>
                        </div>
                        <div class="patient-info">
                            <div class="info-item">
                                <span class="info-label">Email</span>
                                <span class="info-value">${patient.email}</span>
                            </div>
                        </div>
                        <div class="patient-actions">
                            <button class="btn btn-sm btn-outline" onclick="viewPatientDetails(${patient.id})">
                                View Profile
                            </button>
                            <button class="btn btn-sm btn-outline" onclick="viewPatientPredictions(${patient.id})">
                                View Predictions
                            </button>
                            <button class="btn btn-sm btn-primary" onclick="openChatWithPatient(${patient.id})">
                                Chat
                            </button>
                        </div>
                    </div>
                `;
            });

            patientsHtml += '</div>';
            patientsContainer.innerHTML = patientsHtml;

        } catch (error) {
            console.error('Error loading patients:', error);
            showError('Failed to load patients list.');
        }
    }

    // Load consultations tab
    async loadConsultationsTab() {
        try {
            const consultationsContainer = document.getElementById('consultationsList');
            showSkeletonText(consultationsContainer, 5);

            // For now, use the data loaded during initialization
            if (!this.doctorData || !this.doctorData.consultations.length) {
                consultationsContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No consultations available.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let consultationsHtml = `
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th>Patient</th>
                            <th>Prediction</th>
                            <th>Confidence</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            this.doctorData.consultations.forEach(consultation => {
                const riskLevel = consultation.prediction_result === 1 ? 'High Risk' : 'Low Risk';
                const riskClass = consultation.prediction_result === 1 ? 'risk-high' : 'risk-low';
                const date = new Date(consultation.created_at).toLocaleDateString();
                
                consultationsHtml += `
                    <tr>
                        <td>${consultation.username}</td>
                        <td><span class="${riskClass}">${riskLevel}</span></td>
                        <td>${(consultation.confidence_score * 100).toFixed(1)}%</td>
                        <td>${date}</td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="viewConsultationDetails(${consultation.id})">
                                Details
                            </button>
                            <button class="btn btn-sm btn-primary" onclick="openChatWithPatient(${consultation.user_id})">
                                Chat
                            </button>
                        </td>
                    </tr>
                `;
            });

            consultationsHtml += `
                    </tbody>
                </table>
            `;

            consultationsContainer.innerHTML = consultationsHtml;

        } catch (error) {
            console.error('Error loading consultations:', error);
            showError('Failed to load consultations.');
        }
    }

    // Load chat tab
    loadChatTab() {
        // Chat functionality is handled by the chat panel
        // Just ensure the chat panel is available
    }

    // Load reports tab
    loadReportsTab() {
        const reportsContainer = document.getElementById('reportsContent');
        reportsContainer.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h4>Coming Soon</h4>
                    <p>Advanced reporting features will be available in future updates.</p>
                </div>
            </div>
        `;
    }

    // Search patients
    async searchPatients(query) {
        if (this.currentTab !== 'patients') return;

        try {
            const patientsContainer = document.getElementById('patientsList');
            showSkeletonText(patientsContainer, 3);

            let patients;
            if (query.trim()) {
                patients = await searchPatients(query);
            } else {
                patients = await getAssignedUsers();
            }
            
            if (!patients || patients.length === 0) {
                patientsContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No patients found${query ? ` for "${query}"` : ''}.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let patientsHtml = '<div class="patient-list">';
            
            patients.forEach(patient => {
                patientsHtml += `
                    <div class="patient-card">
                        <div class="patient-header">
                            <div class="patient-name">${patient.username}</div>
                            <div class="patient-id">ID: ${patient.id}</div>
                        </div>
                        <div class="patient-info">
                            <div class="info-item">
                                <span class="info-label">Email</span>
                                <span class="info-value">${patient.email}</span>
                            </div>
                        </div>
                        <div class="patient-actions">
                            <button class="btn btn-sm btn-outline" onclick="viewPatientDetails(${patient.id})">
                                View Profile
                            </button>
                            <button class="btn btn-sm btn-outline" onclick="viewPatientPredictions(${patient.id})">
                                View Predictions
                            </button>
                            <button class="btn btn-sm btn-primary" onclick="openChatWithPatient(${patient.id})">
                                Chat
                            </button>
                        </div>
                    </div>
                `;
            });

            patientsHtml += '</div>';
            patientsContainer.innerHTML = patientsHtml;

        } catch (error) {
            console.error('Error searching patients:', error);
            showError('Failed to search patients.');
        }
    }

    // Setup chat functionality
    setupChatFunctionality() {
        // Chat panel toggle
        window.openChatWithPatient = (patientId) => {
            this.chatReceiverId = patientId;
            document.getElementById('chatPanel').style.display = 'flex';
            
            // Update chat header with patient name
            const patient = this.doctorData.assigned_users.find(p => p.id === patientId);
            if (patient) {
                document.getElementById('chatPatientName').textContent = `Chat with ${patient.username}`;
            }
            
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
                showError('No patient selected for chat.');
                return;
            }

            try {
                await sendMessage({
                    receiver_id: this.chatReceiverId,
                    message: message
                });

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
            const messages = await getMessages(this.chatReceiverId);
            const messagesContainer = document.getElementById('chatMessages');
            
            messagesContainer.innerHTML = '';

            messages.forEach(message => {
                const isOwnMessage = message.sender_id == doctorId; // Assuming doctorId is available globally
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
}

// Global function wrappers for inline event handlers
window.viewPatientDetails = (patientId) => {
    // In a real app, this would show detailed patient information
    alert(`Viewing details for patient ID: ${patientId}`);
};

window.viewPatientPredictions = async (patientId) => {
    try {
        const predictions = await getUserPredictions(patientId);
        if (predictions.length === 0) {
            alert(`No prediction history for patient ID: ${patientId}`);
        } else {
            // In a real app, this would show a detailed view of predictions
            alert(`Found ${predictions.length} predictions for patient ID: ${patientId}`);
        }
    } catch (error) {
        console.error('Error loading patient predictions:', error);
        showError('Failed to load patient predictions.');
    }
};

window.viewConsultationDetails = (consultationId) => {
    // In a real app, this would show detailed consultation information
    alert(`Viewing details for consultation ID: ${consultationId}`);
};

window.escalateCase = (patientId) => {
    // In a real app, this would escalate the case to a supervisor
    showWarning(`Case for patient ID: ${patientId} escalated to supervisor.`);
};

// Global doctor dashboard instance
let doctorDashboard = null;

// Initialize doctor dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    doctorDashboard = new DoctorDashboard();
    await doctorDashboard.initialize();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        DoctorDashboard,
        doctorDashboard
    };
}