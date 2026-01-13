// Admin dashboard functionality
class AdminDashboard {
    constructor() {
        this.currentTab = 'dashboard';
        this.adminData = null;
        this.currentUserEditId = null;
        this.currentDoctorEditId = null;
    }

    // Initialize the dashboard
    async initialize() {
        try {
            // Load admin data
            this.adminData = await getAdminDashboard();
            
            // Update UI with admin data
            this.updateUserInfo();
            this.updateDashboardStats();
            this.updateRecentActivity();
            this.updateSystemHealth();
            
            // Set up event listeners
            this.setupEventListeners();
            
            console.log('Admin dashboard initialized successfully');
        } catch (error) {
            console.error('Error initializing admin dashboard:', error);
            showError('Failed to initialize dashboard. Please try refreshing the page.');
        }
    }

    // Update user info in header
    updateUserInfo() {
        // We could fetch admin profile info here if needed
        document.getElementById('userName').textContent = 'Admin';
    }

    // Update dashboard statistics
    updateDashboardStats() {
        if (!this.adminData) return;

        // Update stat elements
        document.getElementById('totalUsers').textContent = this.adminData.stats.users;
        document.getElementById('totalDoctors').textContent = this.adminData.stats.doctors;
        document.getElementById('totalPredictions').textContent = this.adminData.stats.predictions;
        document.getElementById('totalChats').textContent = this.adminData.stats.chats;
    }

    // Update recent activity
    updateRecentActivity() {
        const activityContainer = document.getElementById('recentActivity');
        if (!this.adminData || !this.adminData.recent_activity.length) {
            activityContainer.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <p>No recent activity available.</p>
                    </div>
                </div>
            `;
            return;
        }

        let activityHtml = '<div class="card">';
        activityHtml += '<div class="card-body">';

        this.adminData.recent_activity.forEach(activity => {
            const timestamp = new Date(activity.created_at).toLocaleString();
            const logClass = activity.role === 'admin' ? 'log-info' : 
                           activity.role === 'doctor' ? 'log-warning' : 'log-success';
            
            activityHtml += `
                <div class="log-entry ${logClass}">
                    <div class="log-timestamp">${timestamp}</div>
                    <p class="log-message">
                        User <strong>${activity.username}</strong> (${activity.role}) created
                    </p>
                </div>
            `;
        });

        activityHtml += '</div></div>';
        activityContainer.innerHTML = activityHtml;
    }

    // Update system health
    updateSystemHealth() {
        const healthContainer = document.getElementById('systemHealth');
        // This would be updated with real system health metrics in a production system
        healthContainer.innerHTML = `
            <div class="stat-card">
                <div class="stat-number">🟢</div>
                <div class="stat-label">System Status: Operational</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Uptime</div>
            </div>
        `;
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

        // User management form
        const addUserForm = document.getElementById('addUserForm');
        if (addUserForm) {
            addUserForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddUser(e);
            });
        }

        // Role selection to show/hide specialization
        const roleSelect = document.querySelector('select[name="role"]');
        if (roleSelect) {
            roleSelect.addEventListener('change', (e) => {
                const specializationField = document.getElementById('specializationField');
                specializationField.style.display = e.target.value === 'doctor' ? 'block' : 'none';
            });
        }

        // Assignment form
        const assignForm = document.getElementById('assignForm');
        if (assignForm) {
            assignForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAssignment(e);
            });
        }

        // Search functionality
        this.setupSearchFunctionality();
    }

    // Set up search functionality
    setupSearchFunctionality() {
        const userSearch = document.getElementById('userSearch');
        if (userSearch) {
            userSearch.addEventListener('input', this.debounce((e) => {
                this.searchUsers(e.target.value);
            }, 300));
        }

        const doctorSearch = document.getElementById('doctorSearch');
        if (doctorSearch) {
            doctorSearch.addEventListener('input', this.debounce((e) => {
                this.searchDoctors(e.target.value);
            }, 300));
        }

        const assignmentSearch = document.getElementById('assignmentSearch');
        if (assignmentSearch) {
            assignmentSearch.addEventListener('input', this.debounce((e) => {
                this.searchAssignments(e.target.value);
            }, 300));
        }

        const logSearch = document.getElementById('logSearch');
        if (logSearch) {
            logSearch.addEventListener('input', this.debounce((e) => {
                this.searchLogs(e.target.value);
            }, 300));
        }
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
            case 'users':
                this.loadUsersTab();
                break;
            case 'doctors':
                this.loadDoctorsTab();
                break;
            case 'assignments':
                this.loadAssignmentsTab();
                break;
            case 'logs':
                this.loadLogsTab();
                break;
        }
    }

    // Load users tab
    async loadUsersTab() {
        try {
            const usersContainer = document.getElementById('usersTableBody');
            showSkeletonText(usersContainer.parentElement, 3);

            const users = await getAllUsers();
            
            if (!users || users.length === 0) {
                usersContainer.innerHTML = `
                    <tr>
                        <td colspan="6">No users found.</td>
                    </tr>
                `;
                return;
            }

            let usersHtml = '';
            
            users.forEach(user => {
                const date = new Date(user.created_at).toLocaleDateString();
                
                usersHtml += `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.username}</td>
                        <td>${user.email}</td>
                        <td><span class="badge badge-${user.role === 'admin' ? 'primary' : user.role === 'doctor' ? 'warning' : 'info'}">${user.role}</span></td>
                        <td>${date}</td>
                        <td class="table-actions">
                            <button class="btn btn-sm btn-outline" onclick="editUser(${user.id})">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteUserById(${user.id}, '${user.username}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            usersContainer.innerHTML = usersHtml;

        } catch (error) {
            console.error('Error loading users:', error);
            showError('Failed to load users list.');
        }
    }

    // Load doctors tab
    async loadDoctorsTab() {
        try {
            const doctorsContainer = document.getElementById('doctorsTableBody');
            showSkeletonText(doctorsContainer.parentElement, 3);

            const doctors = await getAllDoctors();
            
            if (!doctors || doctors.length === 0) {
                doctorsContainer.innerHTML = `
                    <tr>
                        <td colspan="7">No doctors found.</td>
                    </tr>
                `;
                return;
            }

            let doctorsHtml = '';
            
            doctors.forEach(doctor => {
                const date = new Date(doctor.created_at).toLocaleDateString();
                
                doctorsHtml += `
                    <tr>
                        <td>${doctor.id}</td>
                        <td>${doctor.username}</td>
                        <td>${doctor.email}</td>
                        <td>${doctor.specialization || 'N/A'}</td>
                        <td>${doctor.license_number || 'N/A'}</td>
                        <td>${date}</td>
                        <td class="table-actions">
                            <button class="btn btn-sm btn-outline" onclick="editDoctor(${doctor.id})">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteUserById(${doctor.id}, '${doctor.username}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            doctorsContainer.innerHTML = doctorsHtml;

        } catch (error) {
            console.error('Error loading doctors:', error);
            showError('Failed to load doctors list.');
        }
    }

    // Load assignments tab
    async loadAssignmentsTab() {
        try {
            // Load users and doctors for dropdowns
            const users = await getAllUsers();
            const doctors = await getAllDoctors();
            
            // Populate user select
            const userSelect = document.getElementById('userSelect');
            userSelect.innerHTML = '<option value="">Select User</option>';
            users.filter(u => u.role === 'user').forEach(user => {
                const option = document.createElement('option');
                option.value = user.id;
                option.textContent = `${user.username} (${user.id})`;
                userSelect.appendChild(option);
            });
            
            // Populate doctor select
            const doctorSelect = document.getElementById('doctorSelect');
            doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
            doctors.forEach(doctor => {
                const option = document.createElement('option');
                option.value = doctor.id;
                option.textContent = `${doctor.username} (${doctor.id})`;
                doctorSelect.appendChild(option);
            });

            // Load assignments
            await this.loadCurrentAssignments();

        } catch (error) {
            console.error('Error loading assignments:', error);
            showError('Failed to load assignments.');
        }
    }

    // Load current assignments
    async loadCurrentAssignments() {
        try {
            const assignmentsContainer = document.getElementById('assignmentsTableBody');
            showSkeletonText(assignmentsContainer.parentElement, 2);

            // In a real app, we'd have an API endpoint for assignments
            // For now, we'll simulate this with a combination of users and doctors
            const users = await getAllUsers();
            const doctors = await getAllDoctors();
            
            // Mock assignments data - in real app this would come from an API
            const assignments = [];
            
            // Simulate some assignments (in a real app, this would be from a dedicated assignments endpoint)
            if (users.length > 0 && doctors.length > 0) {
                // Create a mock assignment between first user and first doctor
                const firstUser = users.find(u => u.role === 'user');
                const firstDoctor = doctors[0];
                
                if (firstUser && firstDoctor) {
                    assignments.push({
                        user: firstUser.username,
                        doctor: firstDoctor.username,
                        assigned_date: new Date().toISOString().split('T')[0]
                    });
                }
            }
            
            if (assignments.length === 0) {
                assignmentsContainer.innerHTML = `
                    <tr>
                        <td colspan="4">No assignments found.</td>
                    </tr>
                `;
                return;
            }

            let assignmentsHtml = '';
            
            assignments.forEach(assignment => {
                assignmentsHtml += `
                    <tr>
                        <td>${assignment.user}</td>
                        <td>${assignment.doctor}</td>
                        <td>${assignment.assigned_date}</td>
                        <td class="table-actions">
                            <button class="btn btn-sm btn-danger" onclick="removeAssignment('${assignment.user}', '${assignment.doctor}')">
                                Remove
                            </button>
                        </td>
                    </tr>
                `;
            });

            assignmentsContainer.innerHTML = assignmentsHtml;

        } catch (error) {
            console.error('Error loading current assignments:', error);
            showError('Failed to load current assignments.');
        }
    }

    // Load logs tab
    async loadLogsTab() {
        try {
            const logsContainer = document.getElementById('logsContainer');
            showSkeletonText(logsContainer, 5);

            const logs = await getSystemLogs();
            
            if (!logs || !logs.logs || logs.logs.length === 0) {
                logsContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No system logs available.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let logsHtml = '<div class="card"><div class="card-body">';

            logs.logs.forEach(log => {
                const logClass = log.level === 'INFO' ? 'log-info' :
                               log.level === 'SUCCESS' ? 'log-success' :
                               log.level === 'WARNING' ? 'log-warning' : 'log-error';
                
                logsHtml += `
                    <div class="log-entry ${logClass}">
                        <div class="log-timestamp">${log.timestamp}</div>
                        <p class="log-message">
                            <strong>${log.level}:</strong> ${log.message}
                        </p>
                    </div>
                `;
            });

            logsHtml += '</div></div>';
            logsContainer.innerHTML = logsHtml;

        } catch (error) {
            console.error('Error loading logs:', error);
            showError('Failed to load system logs.');
        }
    }

    // Handle adding a user
    async handleAddUser(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);

        try {
            // Show loading state
            showSpinnerInButton(submitBtn);

            const userData = Object.fromEntries(formData.entries());
            
            // Convert role to lowercase for consistency
            userData.role = userData.role.toLowerCase();

            // Create user
            const result = await createUser(userData);

            if (result.success) {
                showSuccess(`User ${userData.username} created successfully!`);
                
                // Reset form
                form.reset();
                
                // Hide specialization field if role is not doctor
                document.getElementById('specializationField').style.display = 'none';
                
                // Reload users tab if currently active
                if (this.currentTab === 'users') {
                    await this.loadUsersTab();
                }
            } else {
                showError(result.message || 'Failed to create user.');
            }
        } catch (error) {
            console.error('Error creating user:', error);
            showError('Failed to create user. Please try again.');
        } finally {
            // Restore button
            restoreButton(submitBtn);
        }
    }

    // Handle assignment
    async handleAssignment(event) {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);

        try {
            // Show loading state
            showSpinnerInButton(submitBtn);

            const assignmentData = Object.fromEntries(formData.entries());
            
            // Convert IDs to numbers
            assignmentData.user_id = parseInt(assignmentData.userId);
            assignmentData.doctor_id = parseInt(assignmentData.doctorId);

            // Assign user to doctor
            const result = await assignUserToDoctor(assignmentData);

            if (result.success) {
                showSuccess('Assignment created successfully!');
                
                // Reset form
                form.reset();
                
                // Reload assignments
                await this.loadCurrentAssignments();
            } else {
                showError(result.message || 'Failed to create assignment.');
            }
        } catch (error) {
            console.error('Error creating assignment:', error);
            showError('Failed to create assignment. Please try again.');
        } finally {
            // Restore button
            restoreButton(submitBtn);
        }
    }

    // Search users
    async searchUsers(query) {
        if (this.currentTab !== 'users') return;

        try {
            const usersContainer = document.getElementById('usersTableBody');
            showSkeletonText(usersContainer.parentElement, 2);

            // In a real app, we'd have a search endpoint
            // For now, we'll just reload the users list
            const users = await getAllUsers();
            
            // Filter users based on query
            const filteredUsers = query ? 
                users.filter(user => 
                    user.username.toLowerCase().includes(query.toLowerCase()) ||
                    user.email.toLowerCase().includes(query.toLowerCase())
                ) : users;
            
            if (!filteredUsers || filteredUsers.length === 0) {
                usersContainer.innerHTML = `
                    <tr>
                        <td colspan="6">No users found${query ? ` for "${query}"` : ''}.</td>
                    </tr>
                `;
                return;
            }

            let usersHtml = '';
            
            filteredUsers.forEach(user => {
                const date = new Date(user.created_at).toLocaleDateString();
                
                usersHtml += `
                    <tr>
                        <td>${user.id}</td>
                        <td>${user.username}</td>
                        <td>${user.email}</td>
                        <td><span class="badge badge-${user.role === 'admin' ? 'primary' : user.role === 'doctor' ? 'warning' : 'info'}">${user.role}</span></td>
                        <td>${date}</td>
                        <td class="table-actions">
                            <button class="btn btn-sm btn-outline" onclick="editUser(${user.id})">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteUserById(${user.id}, '${user.username}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            usersContainer.innerHTML = usersHtml;

        } catch (error) {
            console.error('Error searching users:', error);
            showError('Failed to search users.');
        }
    }

    // Search doctors
    async searchDoctors(query) {
        if (this.currentTab !== 'doctors') return;

        try {
            const doctorsContainer = document.getElementById('doctorsTableBody');
            showSkeletonText(doctorsContainer.parentElement, 2);

            // In a real app, we'd have a search endpoint
            // For now, we'll just reload the doctors list
            const doctors = await getAllDoctors();
            
            // Filter doctors based on query
            const filteredDoctors = query ? 
                doctors.filter(doctor => 
                    doctor.username.toLowerCase().includes(query.toLowerCase()) ||
                    doctor.email.toLowerCase().includes(query.toLowerCase()) ||
                    (doctor.specialization && doctor.specialization.toLowerCase().includes(query.toLowerCase()))
                ) : doctors;
            
            if (!filteredDoctors || filteredDoctors.length === 0) {
                doctorsContainer.innerHTML = `
                    <tr>
                        <td colspan="7">No doctors found${query ? ` for "${query}"` : ''}.</td>
                    </tr>
                `;
                return;
            }

            let doctorsHtml = '';
            
            filteredDoctors.forEach(doctor => {
                const date = new Date(doctor.created_at).toLocaleDateString();
                
                doctorsHtml += `
                    <tr>
                        <td>${doctor.id}</td>
                        <td>${doctor.username}</td>
                        <td>${doctor.email}</td>
                        <td>${doctor.specialization || 'N/A'}</td>
                        <td>${doctor.license_number || 'N/A'}</td>
                        <td>${date}</td>
                        <td class="table-actions">
                            <button class="btn btn-sm btn-outline" onclick="editDoctor(${doctor.id})">
                                Edit
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="deleteUserById(${doctor.id}, '${doctor.username}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `;
            });

            doctorsContainer.innerHTML = doctorsHtml;

        } catch (error) {
            console.error('Error searching doctors:', error);
            showError('Failed to search doctors.');
        }
    }

    // Search assignments
    async searchAssignments(query) {
        if (this.currentTab !== 'assignments') return;
        
        // For now, just reload assignments
        await this.loadCurrentAssignments();
    }

    // Search logs
    async searchLogs(query) {
        if (this.currentTab !== 'logs') return;

        try {
            const logsContainer = document.getElementById('logsContainer');
            showSkeletonText(logsContainer, 3);

            const logs = await getSystemLogs();
            
            // Filter logs based on query
            const filteredLogs = query ? 
                logs.logs.filter(log => 
                    log.message.toLowerCase().includes(query.toLowerCase()) ||
                    log.level.toLowerCase().includes(query.toLowerCase())
                ) : logs.logs;
            
            if (!filteredLogs || filteredLogs.length === 0) {
                logsContainer.innerHTML = `
                    <div class="card">
                        <div class="card-body">
                            <p>No logs found${query ? ` for "${query}"` : ''}.</p>
                        </div>
                    </div>
                `;
                return;
            }

            let logsHtml = '<div class="card"><div class="card-body">';

            filteredLogs.forEach(log => {
                const logClass = log.level === 'INFO' ? 'log-info' :
                               log.level === 'SUCCESS' ? 'log-success' :
                               log.level === 'WARNING' ? 'log-warning' : 'log-error';
                
                logsHtml += `
                    <div class="log-entry ${logClass}">
                        <div class="log-timestamp">${log.timestamp}</div>
                        <p class="log-message">
                            <strong>${log.level}:</strong> ${log.message}
                        </p>
                    </div>
                `;
            });

            logsHtml += '</div></div>';
            logsContainer.innerHTML = logsHtml;

        } catch (error) {
            console.error('Error searching logs:', error);
            showError('Failed to search logs.');
        }
    }
}

// Global function wrappers for inline event handlers
window.editUser = (userId) => {
    // In a real app, this would open an edit user modal
    alert(`Editing user ID: ${userId}`);
};

window.editDoctor = (doctorId) => {
    // In a real app, this would open an edit doctor modal
    alert(`Editing doctor ID: ${doctorId}`);
};

window.deleteUserById = async (userId, username) => {
    if (confirm(`Are you sure you want to delete user "${username}"? This action cannot be undone.`)) {
        try {
            await deleteUser(userId);
            showSuccess(`User "${username}" deleted successfully!`);
            
            // Reload current tab
            const adminDash = window.adminDashboard;
            if (adminDash) {
                if (adminDash.currentTab === 'users') {
                    await adminDash.loadUsersTab();
                } else if (adminDash.currentTab === 'doctors') {
                    await adminDash.loadDoctorsTab();
                }
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            showError('Failed to delete user. Please try again.');
        }
    }
};

window.removeAssignment = (userName, doctorName) => {
    if (confirm(`Are you sure you want to remove the assignment between ${userName} and ${doctorName}?`)) {
        // In a real app, this would make an API call to remove the assignment
        showInfo(`Assignment removal between ${userName} and ${doctorName} would occur here.`);
    }
};

window.openAssignmentModal = () => {
    document.getElementById('assignmentModal').style.display = 'flex';
};

window.closeAssignmentModal = () => {
    document.getElementById('assignmentModal').style.display = 'none';
};

window.confirmAssignment = async () => {
    // In a real app, this would confirm the assignment
    closeAssignmentModal();
    showSuccess('Assignment confirmed successfully!');
    
    // Reload assignments
    if (window.adminDashboard) {
        await window.adminDashboard.loadCurrentAssignments();
    }
};

// Global admin dashboard instance
let adminDashboard = null;

// Initialize admin dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    adminDashboard = new AdminDashboard();
    await adminDashboard.initialize();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AdminDashboard,
        adminDashboard
    };
}