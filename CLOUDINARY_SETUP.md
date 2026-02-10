# 🖼️ Cloudinary Setup Guide for LittleLoop

## Why Cloudinary?
Render uses **ephemeral storage** - all uploaded files (media) are deleted on every redeploy. Cloudinary provides **free persistent cloud storage** for your images.

---

## 📝 Setup Steps (5 minutes)

### 1. Create Free Cloudinary Account
1. Go to: https://cloudinary.com/users/register_free
2. Sign up (it's **100% FREE** - no credit card needed)
3. Verify your email

### 2. Get Your Credentials
1. Login to: https://cloudinary.com/console
2. You'll see a dashboard with these credentials:
   - **Cloud Name**: (e.g., `dxy12345`)
   - **API Key**: (e.g., `123456789012345`)
   - **API Secret**: (e.g., `abcdefg_HIJKLMNOP`)

### 3. Add to Render Environment Variables
1. Go to your Render dashboard: https://dashboard.render.com/
2. Click on your **LittleLoop** web service
3. Go to **Environment** tab
4. Click **Add Environment Variable** and add these 3 variables:

```
CLOUDINARY_CLOUD_NAME = <your-cloud-name>
CLOUDINARY_API_KEY = <your-api-key>
CLOUDINARY_API_SECRET = <your-api-secret>
```

5. Click **Save Changes** (Render will auto-redeploy)

---

## ✅ That's It!

After the redeploy:
- All **new uploads** will go to Cloudinary ☁️
- Images will **persist across deployments** 🎉
- Your local development will still use `/media/` folder

---

## 📊 Free Tier Limits
- **25 GB storage** (plenty for your app!)
- **25 GB bandwidth/month**
- No credit card required

---

## 🔧 How It Works

**Local (DEBUG=True):**
- Images save to `/media/` folder on your computer

**Production (DEBUG=False on Render):**
- Images automatically upload to Cloudinary
- Django generates Cloudinary URLs
- Images persist forever (even after redeployment)

---

## ⚠️ Important Note
Your **existing images** on Render are lost (ephemeral storage). After setup, you'll need to:
1. Re-upload test items with images
2. Update profile pictures

All future uploads will be safe! 🚀
