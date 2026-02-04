# LittleLoop 🍼

A peer-to-peer platform connecting parents to donate or sell used baby clothes.

## 📋 Project Overview

**LittleLoop** helps parents:
- 🎁 Donate baby clothes their children have outgrown
- 💰 Sell used baby clothes to other parents
- 🤝 Connect directly with other parents (peer-to-peer)
- 🌍 Arrange their own meetups or delivery

**Note**: LittleLoop is a connection platform only. We don't handle payments, deliveries, or logistics.

## 🛠 Tech Stack

- **Backend**: Django 5.0 (MVT Architecture)
- **Database**: PostgreSQL
- **Authentication**: Google OAuth (via django-allauth)
- **Frontend**: Django Templates + Bootstrap 5
- **Language**: Python 3.11

## ✨ Current Features

- ✅ Google OAuth Authentication
- ✅ Beautiful Bootstrap 5 UI
- ✅ Responsive design
- ✅ Profile completion flow (placeholder)
- ✅ User-friendly landing page

## 📁 Project Structure

```
LittleLoop/
├── accounts/              # Authentication & profile management
├── config/               # Project settings
├── templates/            # Django templates
│   ├── account/         # Login/logout templates
│   ├── accounts/        # Profile templates
│   ├── base.html        # Base template
│   └── home.html        # Landing page
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (running on port 5433)
- Google OAuth credentials

### Installation

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Database: `littleloop`
   - User: `postgres`
   - Password: `admin`
   - Host: `localhost`
   - Port: `5433`

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start server**
   ```bash
   python manage.py runserver
   ```

6. **Access application**
   - Homepage: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## 🔐 OAuth Setup

### Google Authentication (Working)

1. Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
3. Configure via Django Admin:
   - Go to: http://localhost:8000/admin/
   - Sites → Update domain to `localhost:8000`
   - Social applications → Add Google app with your credentials

### Facebook Authentication (Optional - Not configured)

Facebook requires HTTPS for local development. To enable:
1. Install: `pip install django-sslserver`
2. Run: `python manage.py runsslserver`
3. Configure Facebook app with HTTPS redirect URIs

## 🎯 Next Steps (STEP 3)

- [ ] Create UserProfile model
- [ ] Build profile completion form
- [ ] Activate middleware to enforce profile completion
- [ ] Create user dashboard

## 📝 Development Notes

### Feature-Based Architecture
- Each feature has its own Django app
- Current apps: `accounts` (authentication)
- Future apps: `listings`, `messaging`, `reviews`, `search`

### Authentication Flow
```
User → Login Page → Google OAuth → Profile Completion → Home
```

## 🔒 Security

- CSRF protection enabled
- SQL injection protection (Django ORM)
- XSS protection (Django templates)
- OAuth state verification
- Session security

## 🤝 Contributing

This is a personal project for educational purposes.

## 📄 License

This project is for educational/personal use.

---

**Built with Django MVT Architecture**
