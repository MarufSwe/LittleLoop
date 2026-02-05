# Mobile Testing & OAuth Setup Guide

## 🚨 Issue: Google Login Not Working on Mobile

### Problem
- Mobile shows "information not secure" warning
- After clicking "send anyway", shows "Access blocked: authorization error"
- Works fine on laptop

### Root Cause
Google OAuth requires **HTTPS** for mobile devices. HTTP (localhost) works on desktop but not on mobile due to stricter security policies.

---

## ✅ Solution: Use ngrok for HTTPS Tunnel

### Step 1: Install ngrok

**Mac:**
```bash
brew install ngrok
```

**Windows/Linux:**
Download from: https://ngrok.com/download

### Step 2: Start Django Server
```bash
cd /Users/kmaruf/Mine/Projects/LittleLoop
source venv/bin/activate
python manage.py runserver
```

### Step 3: Create HTTPS Tunnel (New Terminal)
```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy this HTTPS URL!** (e.g., `https://abc123.ngrok.io`)

### Step 4: Update Google OAuth Settings

1. Go to: https://console.cloud.google.com/
2. Select your project
3. Navigate to: **APIs & Services** → **Credentials**
4. Click your OAuth 2.0 Client ID
5. Add to **Authorized redirect URIs**:
   ```
   https://abc123.ngrok.io/accounts/google/login/callback/
   ```
   ⚠️ Replace `abc123` with YOUR ngrok subdomain!
6. Click **Save**

### Step 5: Update Django Site Domain

**Option A: Via Django Shell**
```bash
python manage.py shell
```

Then run:
```python
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'abc123.ngrok.io'  # YOUR ngrok domain (no https://)
site.name = 'LittleLoop'
site.save()
exit()
```

**Option B: Via Django Admin**
1. Go to: `https://abc123.ngrok.io/admin/`
2. Click **Sites**
3. Click the site (usually "example.com")
4. Change:
   - Domain name: `abc123.ngrok.io` (no https://)
   - Display name: `LittleLoop`
5. Click **Save**

### Step 6: Test on Mobile

1. Open mobile browser
2. Go to: `https://abc123.ngrok.io`
3. Click Login
4. Choose Google
5. Should work now! ✅

---

## 📱 Mobile Responsiveness - Already Implemented!

### What's Responsive:

✅ **Navbar**
- Collapses to hamburger menu on mobile
- Full-width buttons when expanded
- Compact logo and profile image

✅ **Hero Section**
- Adaptive text sizes:
  - Desktop: 2.8rem
  - Tablet: 2.2rem
  - Mobile: 1.8rem
  - Small mobile: 1.6rem

✅ **Filter Card**
- Filters stack vertically on mobile
- Smaller text and padding on mobile
- Filter buttons go full width
- Results badge scales down

✅ **Item Cards**
- Grid adapts automatically:
  - Desktop (XL): 4 columns
  - Laptop (LG): 3 columns
  - Tablet (MD): 2 columns
  - Mobile (SM): 1 column
- Image carousel works with touch swipe
- Badges stack when needed
- All text scales appropriately

✅ **Forms**
- All inputs full width on mobile
- Touch-friendly button sizes
- Proper spacing for fat fingers

---

## 🧪 Test Checklist

### Desktop (Already Working ✅)
- [x] Google login
- [x] Browse items
- [x] Post items
- [x] Edit items
- [x] My Items page

### Mobile (After ngrok setup)
- [ ] Open `https://your-ngrok-url.ngrok.io` on phone
- [ ] Google login should work
- [ ] Browse items (swipe through images)
- [ ] Responsive layout looks good
- [ ] Navbar collapses properly
- [ ] Filters work
- [ ] Post item form is usable
- [ ] Profile page looks good

---

## 💡 Tips

### Keep ngrok Running
- ngrok must stay running while testing
- Each time you restart ngrok, you get a new URL
- Free plan gives you a random URL each time
- Paid plan ($8/mo) gives you a fixed subdomain

### Switching Back to Localhost
When done with mobile testing, switch back:

```python
# Django shell
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = '127.0.0.1:8000'
site.save()
```

### Alternative: Deploy to Production
For permanent mobile testing, deploy to a real HTTPS server:
- Heroku (free tier)
- PythonAnywhere
- DigitalOcean
- AWS
- Vercel + Railway

---

## 📋 Quick Reference

### Current Setup (Localhost)
- URL: `http://127.0.0.1:8000`
- Works on: Desktop only
- Google OAuth: Works
- Mobile: ❌ Doesn't work

### With ngrok (HTTPS Tunnel)
- URL: `https://abc123.ngrok.io`
- Works on: Desktop + Mobile
- Google OAuth: Works everywhere
- Mobile: ✅ Works!

---

## 🔧 Troubleshooting

### "This site can't be reached" on mobile
- Make sure ngrok is running
- Check you're using HTTPS URL (not HTTP)
- Ensure phone is on same network OR use cellular

### "Authorization error" still appears
- Double-check redirect URI in Google Console
- Make sure Site domain in Django matches ngrok URL (without https://)
- Clear browser cache on mobile
- Try incognito/private browsing

### ngrok session expired
- Free plan: 2 hour sessions
- Just restart: `ngrok http 8000`
- Update Google Console with new URL
- Update Django Site with new domain

---

**Your site is fully responsive and ready for mobile!** 📱✨

Just follow the ngrok setup above to enable mobile Google login.
