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

### Authentication & Profile
- ✅ Google OAuth Authentication (Facebook optional)
- ✅ Mandatory profile completion after first login
- ✅ User profile with photo, phone, location, bio
- ✅ Profile dropdown navigation

### Marketplace (Core Features)
- ✅ **Public Homepage** - Browse items without login
- ✅ **Item Listings** - Grid view of all donate/sell items
- ✅ **Advanced Filters** - Filter by type, gender, age range, area
- ✅ **Item Details** - Full item information page
- ✅ **Contact System** - View owner's phone after login
- ✅ **Post Items** - Create donate/sell listings (login required)
- ✅ **My Items** - Manage your posted items
- ✅ **Mark as Done** - Remove items from listing

### UI/UX
- ✅ Beautiful Bootstrap 5 design
- ✅ Fully responsive layout
- ✅ Real-time image preview
- ✅ Hover effects and animations
- ✅ Mobile-friendly navigation

## 📁 Project Structure

```
LittleLoop/
├── accounts/              # Authentication & profile management
├── listings/              # Baby clothes marketplace
├── config/               # Project settings
├── templates/            # Django templates
│   ├── account/         # Login/logout templates
│   ├── accounts/        # Profile templates
│   ├── listings/        # Item listing templates
│   ├── base.html        # Base template
├── media/               # User uploads (profile pics, item images)
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
   - Homepage (Browse items): http://localhost:8000/
   - Post Item: http://localhost:8000/create/
   - My Items: http://localhost:8000/my-items/
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

## 🎯 Next Steps

### Potential Enhancements
- [ ] User-to-user messaging system
- [ ] Review and rating system
- [ ] Transaction history tracking
- [ ] Email notifications
- [ ] Advanced search with multiple filters
- [ ] Item favorites/wishlist
- [ ] Facebook login activation (requires HTTPS)

## 📝 Development Notes

### Feature-Based Architecture
- Each feature has its own Django app
- Current apps:
  - `accounts` - Authentication & user profiles
  - `listings` - Item marketplace (donate/sell)
- Future apps: `messaging`, `reviews`, `search`

### Authentication Flow
```
User → Browse Items (Public) → Click Item → Login Required
     → Google OAuth → Profile Completion → View Contact Info
```

### Posting Flow
```
User → Post Item → Login Required → Profile Check
     → Fill Form (Title, Description, Gender, Age, etc.)
     → Choose Donate/Sell → Submit → Item Published
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
