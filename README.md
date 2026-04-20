# 🌾 AgriPrice Portal

AgriPrice Portal is a modern web-based platform built using Flask that connects agricultural sellers with buyers by providing real-time product listings, price management, and news updates.

It includes a complete seller management system, admin dashboard, product handling, and push notification system for real-time updates.

---

## 🚀 Features

### 👨‍🌾 Seller Module
- Seller Registration & Login (OTP Verification)
- Seller Dashboard
- Add / Edit / Delete Products
- Product Search with Autocomplete
- Profile Image Upload

### 🛒 Product Management
- Store products in SQLite database
- Dynamic product listing
- Edit mode with autocomplete search
- Real-time updates

### 📰 News & Notifications
- Admin can upload news
- Firebase Push Notifications
- Notifications shown on mobile & desktop

### 🛠 Admin Panel
- Manage sellers
- Manage products
- Manage companies
- View feedback & reports

### 📂 File Handling System
- Upload images, videos, PDFs
- Preview files
- Download options (Low / Medium / High quality)

### 🌐 Frontend Features
- Responsive UI (HTML, CSS, JS)
- Dark-themed modern design
- AJAX-based real-time updates
- Service Worker (Offline support)

---

## 🧠 Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Realtime:** AJAX
- **Notifications:** Firebase Cloud Messaging
- **Storage:** Local + Static files
- **Service Worker:** Offline support

---

## 📁 Project Structure


AgriPrice Portal/
│── app.py
│── products.db
│── faqs.json
│
├── static/
│ ├── img/
│ ├── temp/
│ ├── firebase-messaging-sw.js
│ ├── service-worker.js
│
├── templates/
│ ├── index.html
│ ├── seller_dashboard.html
│ ├── manage_products.html
│ ├── manage_news.html
│ ├── admin.html
│ └── ...


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/agri-price-portal.git
cd agri-price-portal
2️⃣ Install Dependencies
pip install flask
3️⃣ Run Application
python app.py
4️⃣ Open in Browser
http://127.0.0.1:5000
🔔 Firebase Setup (For Notifications)
Create project in Firebase
Enable Cloud Messaging
Replace config in:
static/firebase-messaging-sw.js
📸 Screenshots

(Add your UI screenshots here)

💡 Future Improvements
Payment integration
AI-based price prediction
Multi-language support
Mobile app using Flutter
Advanced analytics dashboard
👨‍💻 Developed By

A S Shridatta Aigal

📜 License

This project is for educational purposes.


---

# 📌 Project Description (for GitHub)

You can paste this in **GitHub description section**:

> AgriPrice Portal is a Flask-based web application designed to connect agricultural sellers with buyers through real-time product listings, price management, and news updates. It includes seller authentication, admin dashboard, Firebase push notifications, and a modern responsive UI with AJAX-based updates.

---

# 🤖 AI Prompt (VERY IMPORTANT 🔥)

Use this if you want to regenerate your project using AI tools (like ChatGPT, Claude, etc.):

```text
Create a full-stack web application called "AgriPrice Portal" using Python Flask as backend and HTML, CSS, JavaScript as frontend.

Requirements:

1. Authentication System:
- Seller registration with OTP verification
- Login/logout system using Flask session

2. Seller Dashboard:
- Add, edit, delete products
- Product search with autocomplete
- Upload profile image

3. Admin Panel:
- Manage sellers
- Manage products
- Manage companies
- View feedback and reports

4. Product System:
- Store data in SQLite
- Show dynamic product listing
- Edit mode should support autocomplete search input

5. News System:
- Admin uploads news
- Display news to users
- Send push notifications using Firebase Cloud Messaging

6. File Upload System:
- Upload images, videos, PDFs
- Preview files
- Download with options: Low, Medium, High quality

7. Frontend:
- Modern dark theme UI
- Responsive design
- Use AJAX for real-time updates
- Include animations and modals

8. Additional:
- Service worker for offline support
- Clean folder structure (templates, static, etc.)
- No errors in code
- Production-ready project

Output:
- Full working project code
- Organized folder structure
- Ready to run without errors
