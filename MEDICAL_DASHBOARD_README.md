# 🏥 Premium Medical Dashboard Application

A role-based medical web application with real-time chat functionality and heart disease prediction integration.

## 🌟 Features

### User Roles
- **Admin**: System management, user management, assignments
- **Doctor**: Patient management, consultations, predictions review
- **User**: Personal dashboard, prediction requests, chat with doctors

### Core Functionality
- 🔐 Role-based authentication and authorization
- 💬 Real-time chat between users and doctors
- 🫀 Heart disease prediction using ML model
- 📊 Interactive dashboards for each role
- 🎨 Modern UI with dark/light theme support
- 📱 Fully responsive design

### Technical Features
- RESTful API architecture
- SQLite database with user management
- Fetch API for all backend interactions
- Skeleton loaders and animated transitions
- Toast notifications for all important events
- No page reloads after login

## 🏗️ Architecture

### Backend Structure
```
backend/
├── auth.py          # Authentication routes
├── user.py          # User dashboard routes
├── doctor.py        # Doctor dashboard routes
├── admin.py         # Admin dashboard routes
└── chat.py          # Chat functionality routes
```

### Frontend Structure
```
static/
├── css/
│   ├── variables.css    # CSS variables for themes
│   ├── base.css         # Base styles
│   ├── components.css   # Component styles
│   └── animations.css   # Animation styles
└── js/
    ├── api.js              # API client wrapper
    ├── auth.js             # Authentication management
    ├── theme.js            # Theme management
    └── ui/                 # UI components
    │   ├── toast.js        # Toast notifications
    │   └── loader.js       # Loading utilities
    └── dashboards/         # Dashboard-specific JS
    │   ├── user.js
    │   ├── doctor.js
    │   └── admin.js
    └── chat/
        ├── chat-api.js
        └── chat-ui.js
```

### Templates
```
templates/
├── login.html    # Login page
├── user.html     # User dashboard
├── doctor.html   # Doctor dashboard
└── admin.html    # Admin dashboard
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required model files: `heart_disease_model.pkl`, `feature_names.json`

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure model files are in the root directory
4. Run the application: `python run_medical_app.py` or `start_medical_app.bat`

### Default Credentials
- **Admin**: `admin` / `admin123`
- **Doctor**: `doctor1` / `doctor123`
- **User**: `user1` / `user123`

## 🌐 Access Points

- **Login**: http://localhost:5000/login
- **User Dashboard**: http://localhost:5000/user
- **Doctor Dashboard**: http://localhost:5000/doctor
- **Admin Dashboard**: http://localhost:5000/admin

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### User Endpoints
- `GET /api/user/dashboard` - Get user dashboard data
- `POST /api/user/predict` - Make heart disease prediction
- `GET /api/user/predictions/history` - Get prediction history
- `POST /api/user/request_consultation` - Request doctor consultation
- `GET /api/user/assigned_doctor` - Get assigned doctor

### Doctor Endpoints
- `GET /api/doctor/dashboard` - Get doctor dashboard data
- `GET /api/doctor/users` - Get assigned users
- `GET /api/doctor/user/<id>/predictions` - Get user predictions
- `POST /api/doctor/consultation/update_status` - Update consultation status
- `GET /api/doctor/patients/search` - Search patients

### Admin Endpoints
- `GET /api/admin/dashboard` - Get admin dashboard data
- `GET /api/admin/users` - Get all users
- `GET /api/admin/doctors` - Get all doctors
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/<id>` - Update user
- `DELETE /api/admin/users/<id>` - Delete user
- `POST /api/admin/assignments` - Assign user to doctor
- `GET /api/admin/logs` - Get system logs

### Chat Endpoints
- `POST /api/chat/send` - Send message
- `GET /api/chat/messages/<id>` - Get messages with user
- `GET /api/chat/conversations` - Get all conversations
- `POST /api/chat/typing` - Send typing indicator
- `POST /api/chat/mark_delivered/<id>` - Mark message delivered
- `GET /api/chat/admin/logs` - Get chat logs (admin only)

## 🎨 UI/UX Features

### Modern Interactions
- Animated transitions between UI states
- Skeleton loaders during data fetching
- Visual feedback for all user actions
- Loading states for all actions
- Toast notifications for important events
- Smooth scrolling and animations

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Adaptive components
- Touch-friendly controls

### Accessibility
- Proper focus management
- Semantic HTML structure
- Keyboard navigation support
- Screen reader friendly

## 🏥 Medical Dashboard Features

### User Dashboard
- Personal health metrics
- Prediction history
- Chat with assigned doctor
- Risk assessment results
- Recommendations

### Doctor Dashboard
- Patient management
- Consultation tracking
- Critical case alerts
- Patient communication
- Treatment monitoring

### Admin Dashboard
- User management
- Doctor management
- Assignments
- System monitoring
- Activity logs

## 🛡️ Security

- Session-based authentication
- Password hashing with Werkzeug
- Input validation and sanitization
- Role-based access control
- Secure session management

## 📊 Data Models

### Users
- ID, username, password hash, role, email, creation date

### Predictions
- ID, user_id, patient_data, prediction_result, confidence_score, creation date

### Doctors
- ID, user_id, specialization, license_number

### Chats
- ID, sender_id, receiver_id, message, timestamp, status

### Assignments
- ID, user_id, doctor_id, assignment date

## 🔄 Real-time Features

- Polling-based chat updates (no WebSockets needed)
- Automatic message refresh
- Typing indicators
- Delivery status tracking
- Online presence simulation

## 🎯 Core UX Principles Implemented

✅ No full page reloads after login
✅ All backend interactions via fetch() + JSON
✅ Every user action triggers visual feedback
✅ Loading states for all asynchronous operations
✅ Skeleton loaders while waiting for data
✅ Toast notifications for all important events
✅ Animated transitions between UI states
✅ Fully responsive (mobile-first)
✅ Dark/light mode toggle using CSS variables
✅ Interactive elements with hover/focus states
✅ Smooth scrolling and transitions
✅ Form validation and error handling
✅ Success/error response states