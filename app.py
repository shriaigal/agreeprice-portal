from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from datetime import timedelta
from flask_mail import Mail, Message
from datetime import datetime
import pytz  # Make sure pytz is installed
import base64

app = Flask(__name__)
app.secret_key = "shri_aigal"
app.permanent_session_lifetime = timedelta(days=7)

# ====================
# FLASK-MAIL CONFIG
# ====================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aicontentcreator772@gmail.com'
app.config['MAIL_PASSWORD'] = 'qvkj ssnb qjrj hrbl'
app.config['MAIL_DEFAULT_SENDER'] = 'aicontentcreator772@gmail.com'

mail = Mail(app)

# ====================
# DB
# ====================



def get_db_connection():
    conn = sqlite3.connect('products.db', timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')

    c.execute('''
        CREATE TABLE IF NOT EXISTS seller_registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_no TEXT NOT NULL,
            email TEXT NOT NULL,
            gst_no TEXT NOT NULL,
            phone_no TEXT NOT NULL,
            profile_image BLOB NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            seller_id INTEGER NOT NULL,
            FOREIGN KEY (seller_id) REFERENCES seller_registration(id) ON DELETE CASCADE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS report (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT
)
    ''')

    conn.commit()
    conn.close()

# ====================
# HOME
# ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iindex')
def iindex():
    return render_template('index.html')


# ====================
# SELLER LOGIN / LOGOUT
# ====================

@app.route('/seller_login')
def seller_login():
    if session.get('seller_logged_in'):
        return redirect(url_for('seller_dashboard'))
    return render_template('seller_login.html')  # ✅ DON'T redirect to /login here


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('seller_logged_in'):
        return redirect(url_for('seller_dashboard'))

    if request.method == 'POST':
        company_name = request.form['companyName'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id, password FROM seller_registration WHERE company_name = ? AND email = ?', (company_name, email))
        user = c.fetchone()
        conn.close()

        if user:
            user_id, stored_password = user
            if stored_password == password:
                session.permanent = True
                session['seller_logged_in'] = True
                session['seller_id'] = user_id
                flash('Login successful!', 'success')
                return redirect(url_for('seller_dashboard'))
            else:
                flash('Incorrect password.', 'error')
        else:
            flash('Invalid credentials.', 'error')

        return redirect(url_for('seller_login'))

    return render_template('seller_login.html')

@app.route('/seller_logout')
def seller_logout():
    session.pop('seller_logged_in', None)
    session.pop('seller_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('seller_login'))

# ====================
# SELLER DASHBOARD
# ====================





import base64

@app.route('/seller')
def seller_dashboard():
    print("Session status:", session.get('seller_logged_in'))
    if not session.get('seller_logged_in'):
        flash('Please log in as seller.', 'error')
        return redirect(url_for('seller_login'))




    seller_id = session.get('seller_id')
    conn = get_db_connection()
    seller = conn.execute('SELECT * FROM seller_registration WHERE id = ?', (seller_id,)).fetchone()
    conn.close()

    if not seller:
        flash('Seller not found.', 'error')
        return redirect(url_for('seller_login'))

    seller_dict = dict(seller)
    profile_image_data = seller_dict.get('profile_image')

    # Encode only if data is reasonable
    if profile_image_data and len(profile_image_data) < 1_000_000:  # less than 1MB
        seller_dict['profile_image'] = base64.b64encode(profile_image_data).decode('utf-8')
    else:
        seller_dict['profile_image'] = None

    return render_template('seller_dashboard.html', seller=seller_dict)



@app.route('/update_profile_image', methods=['POST'])
def update_profile_image():
    if not session.get('seller_logged_in'):
        flash("Please login first.", "error")
        return redirect(url_for('seller_login'))

    seller_id = session.get('seller_id')  # Use your actual session key
    image_file = request.files.get('profile_image')

    if image_file and image_file.filename != '':
        image_data = image_file.read()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE seller_registration SET profile_image = ? WHERE id = ?", (image_data, seller_id))
        conn.commit()
        conn.close()

        flash("Profile image updated successfully!", "success")
    else:
        flash("No image selected!", "error")

    return redirect(url_for('seller_dashboard'))


# ====================
# SELLER REGISTRATION
# ====================

@app.route('/seller_registration')
def seller_registration():
    return render_template('seller_registration.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        company_name = request.form['companyName']
        company_no = request.form['companyNo']
        email = request.form['email']
        gst_no = request.form['gstNo']
        phone_no = request.form['phoneNo']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(request.url)

        profile_image = request.files['profileImage']
        if profile_image:
            image_data = profile_image.read()
        else:
            flash('Profile image is required.', 'error')
            return redirect(request.url)

        conn = get_db_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO seller_registration
            (company_name, company_no, email, gst_no, phone_no, profile_image, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company_name, company_no, email, gst_no, phone_no, sqlite3.Binary(image_data), password))
        conn.commit()
        conn.close()

        send_welcome_email(company_name, email)
        flash('Company registered successfully!', 'success')
        return redirect(url_for('seller_login'))

    return render_template('seller_registration.html')




# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Step 1: Collect form data
#         company_name = request.form['companyName']
#         company_no = request.form['companyNo']
#         email = request.form['email']
#         gst_no = request.form['gstNo']
#         phone_no = request.form['phoneNo']
#         password = request.form['password']
#         confirm_password = request.form['confirmPassword']
#         profile_image = request.files['profileImage']

#         # Step 2: Basic validation
#         if password != confirm_password:
#             flash('Passwords do not match!', 'error')
#             return redirect(request.url)

#         if not profile_image:
#             flash('Profile image is required.', 'error')
#             return redirect(request.url)

#         # Step 3: Save image temporarily (as before)
#         filename = f"{uuid.uuid4().hex}_{profile_image.filename}"
#         temp_path = os.path.join('static', 'temp', filename)
#         os.makedirs(os.path.dirname(temp_path), exist_ok=True)
#         profile_image.save(temp_path)

#         # Step 4: Store data in session
#         session['registration_data'] = {
#             'company_name': company_name,
#             'company_no': company_no,
#             'email': email,
#             'gst_no': gst_no,
#             'phone_no': phone_no,
#             'password': password,
#             'image_path': temp_path
#         }

#         # Step 5: Send OTP
#         try:
#             client.verify.v2.services(VERIFY_SERVICE_SID).verifications.create(
#                 to='+91' + phone_no,
#                 channel='sms'
#             )
#             flash('OTP sent to your phone number.', 'success')

#             # ✅ Return this after OTP is sent successfully
#             return render_template('verify_otp.html', phone=phone_no)

#         except Exception as e:
#             flash(f"Failed to send OTP: {str(e)}", 'error')
#             return redirect(request.url)

#     # GET request → show registration form
#     return render_template('seller_registration.html')


# import random

# def generate_otp():
#     return str(random.randint(100000, 999999))


# @app.route('/verify-otp', methods=['POST'])
# def verify_otp():
#     otp = request.form['otp']
#     phone = request.form['phone']

#     try:
#         verification_check = client.verify.v2.services(VERIFY_SERVICE_SID) \
#             .verification_checks.create(to='+91' + phone, code=otp)

#         if verification_check.status == 'approved':
#             data = session.pop('registration_data', None)
#             if not data:
#                 flash("Session expired. Please register again.", "error")
#                 return redirect(url_for('register'))

#             # Read image from saved path
#             with open(data['image_path'], 'rb') as img_file:
#                 image_binary = img_file.read()

#             # Clean up temp image
#             os.remove(data['image_path'])

#             # Save to DB
#             conn = get_db_connection()
#             c = conn.cursor()
#             c.execute('''INSERT INTO seller_registration
#                          (company_name, company_no, email, gst_no, phone_no, profile_image, password)
#                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
#                       (data['company_name'], data['company_no'], data['email'], data['gst_no'],
#                        data['phone_no'], sqlite3.Binary(image_binary), data['password']))
#             conn.commit()
#             conn.close()

#             send_welcome_email(data['company_name'], data['email'])

#             flash("OTP Verified! Company registered successfully.", "success")
#             return redirect(url_for('seller_login'))

#         else:
#             flash("Invalid OTP. Please try again.", "error")
#             return render_template("verify_otp.html", phone=phone)

#     except Exception as e:
#         flash(f"OTP verification failed: {str(e)}", "error")
#         return render_template("verify_otp.html", phone=phone)
    

    
# @app.route('/resend-otp', methods=['POST'])
# def resend_otp():
#     phone = request.form.get('phone')

#     try:
#         client.verify.v2.services(VERIFY_SERVICE_SID).verifications.create(
#             to='+91' + phone,
#             channel='sms'
#         )
#         flash('OTP resent successfully.', 'success')
#     except Exception as e:
#         flash(f'Failed to resend OTP: {str(e)}', 'error')

#     return render_template('verify_otp.html', phone=phone)


# ====================
# PRODUCT SUBMIT
# ====================

@app.route('/submit', methods=['POST'])
def submit_product():
    if not session.get('seller_logged_in'):
        flash('Login required.', 'error')
        return redirect(url_for('seller_login'))

    product = request.form['product']
    quantity = request.form['quantity']
    price = request.form['price']
    date = request.form['date']
    location = request.form['location']

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO product (product_name, quantity, price, date, location, seller_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (product, quantity, price, date, location, session['seller_id']))
    conn.commit()
    conn.close()

    flash('Product submitted.', 'success')
    return redirect(url_for('seller_dashboard'))

# ====================
# VIEWER
# ====================

@app.route('/viewer')
def viewer():
    today = '2025-07-14'  # Or use datetime.now().strftime("%Y-%m-%d")
    return render_template('viewer.html', today=today)

@app.route('/get_products', methods=['POST'])
def get_products():
    date_param = request.form['date'].strip()
    location_param = request.form.get('location', 'all').strip()

    print(f"[DEBUG] date: {date_param} | location: {location_param}")

    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    if location_param == 'all':
        c.execute('''
            SELECT p.id, p.product_name, p.quantity, p.price, p.location, s.company_name 
            FROM product p 
            JOIN seller_registration s ON p.seller_id = s.id
            WHERE p.date = ?
        ''', (date_param,))
    else:
        c.execute('''
            SELECT p.id, p.product_name, p.quantity, p.price, p.location, s.company_name 
            FROM product p 
            JOIN seller_registration s ON p.seller_id = s.id
            WHERE p.date = ? AND p.location = ? COLLATE NOCASE
        ''', (date_param, location_param))

    rows = c.fetchall()
    conn.close()

    print(f"[DEBUG] rows found: {len(rows)}")
    return jsonify(rows)


# ====================
# ADMIN
# ====================

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    print(f"Username entered: {username}")
    print(f"Password entered: {password}")

    if username == 'shriaigal@admin' and password == 'shriaigal':
        session.permanent = True
        session['admin_logged_in'] = True
        flash('Admin login successful.', 'success')
    else:
        flash('Invalid admin credentials.', 'danger')

    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin_logged_in', None)
    flash('Logged out.', 'info')
    return redirect(url_for('admin'))



# Manage companies
@app.route('/manage_companies')
def manage_companies():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM seller_registration')
    companies = c.fetchall()
    conn.close()
    return render_template('manage_companies.html', companies=companies)


# Manage products
@app.route('/manage_products')
def manage_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
    SELECT p.id, p.product_name, p.quantity, p.price, p.date, 
           s.company_name, s.company_no, s.email
    FROM product p
    JOIN seller_registration s ON p.seller_id = s.id
''')

    products = c.fetchall()
    conn.close()
    return render_template('manage_products.html', products=products)


# Delete company
@app.route('/delete_company/<int:id>')
def delete_company(id):
    conn = sqlite3.connect('products.db')
    conn.execute('PRAGMA foreign_keys = ON')
    c = conn.cursor()
    c.execute('DELETE FROM seller_registration WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Company deleted successfully!')
    return redirect(url_for('manage_companies'))


# Delete product
@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('DELETE FROM product WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Product deleted successfully!')
    return redirect(url_for('manage_products'))


# Edit company
@app.route('/edit_company/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_no = request.form['company_no']
        email = request.form['email']
        gst_no = request.form['gst_no']
        phone_no = request.form['phone_no']
        c.execute('''
            UPDATE seller_registration 
            SET company_name=?, company_no=?, email=?, gst_no=?, phone_no=?
            WHERE id=?
        ''', (company_name, company_no, email, gst_no, phone_no, id))
        conn.commit()
        conn.close()
        flash('Company updated successfully!')
        return redirect(url_for('manage_companies'))
    else:
        c.execute('SELECT * FROM seller_registration WHERE id = ?', (id,))
        company = c.fetchone()
        conn.close()
        return render_template('edit_company.html', company=company)


# Edit product
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        price = request.form['price']
        date = request.form['date']
        c.execute('''
            UPDATE product 
            SET product_name=?, quantity=?, price=?, date=?
            WHERE id=?
        ''', (product_name, quantity, price, date, id))
        conn.commit()
        conn.close()
        flash('Product updated successfully!')
        return redirect(url_for('manage_products'))
    else:
        c.execute('SELECT * FROM product WHERE id = ?', (id,))
        product = c.fetchone()
        conn.close()
        return render_template('edit_product.html', product=product)


# API updates
@app.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):
    data = request.get_json()
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
        UPDATE product
        SET product_name = ?, quantity = ?, price = ?, date = ?
        WHERE id = ?
    ''', (data['product_name'], data['quantity'], data['price'], data['date'], id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/update_company/<int:id>', methods=['POST'])
def update_company(id):
    data = request.get_json()
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
        UPDATE seller_registration 
        SET company_name = ?, company_no = ?, email = ?, gst_no = ?, phone_no = ?
        WHERE id = ?
    ''', (data['company_name'], data['company_no'], data['email'], data['gst_no'], data['phone_no'], id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ====================
# FORGOT PASSWORD
# ====================

@app.route('/forgot')
def forgote():
    return render_template('forgotpassword.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_no = request.form['company_no']
        email = request.form['email']
        new_password = request.form['new_password']
        conn = sqlite3.connect('products.db')
        c = conn.cursor()

        # Check if record exists
        c.execute('SELECT * FROM seller_registration WHERE company_name = ? AND company_no = ? AND email = ?',
                  (company_name, company_no, email))
        user = c.fetchone()

        if user:
            # Update the password
            c.execute('UPDATE seller_registration SET password = ? WHERE company_name = ? AND company_no = ? AND email = ?',
                      (new_password, company_name, company_no, email))
            conn.commit()
            conn.close()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('seller_login'))
        else:
            conn.close()
            flash('Details not found. Please check your information.', 'error')
            return redirect(url_for('forgot_password'))

    return render_template('forgotpassword.html')

# ====================
# FEEDBACK & REPORT
# ====================

def send_welcome_email(company_name, recipient_email):
    try:
        msg = Message(
            subject=f"Welcome to AgriPrice Portal, {company_name}!",
            recipients=[recipient_email],
            body=f"""
Hello {company_name},

Welcome to our website!
Thank you for registering your company with AgriPrice Portal.

We’re happy to have you on board. With your new account, you can:
- Post and manage your product listings
- Check the latest market prices
- Connect with verified buyers and sellers
- Grow your business in the agricultural market

Next Steps:
👉 Log in to your account: https://agripriceportal.pythonanywhere.com//seller
👉 Update your company profile: https://agripriceportal.pythonanywhere.com//seller

If you have any questions or queries, please visit our website and submit your feedback. If you face any issues, you can also report them directly on the website.

Thank you again for choosing us. We look forward to supporting your company’s growth!

Best wishes,
The AgriPrice Portal Team
https://agripriceportal.pythonanywhere.com/
"""
        )
        mail.send(msg)
        print(f"Welcome email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending welcome email: {e}")

#mails report and feedback
@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    data = request.get_json()
    user_email = data.get('email')
    user_message = data.get('message')

    # ✅ Save to DB
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (user_email, message) VALUES (?, ?)', (user_email, user_message))
    conn.commit()
    conn.close()

    try:
        msg = Message(
            subject="New Feedback",
            recipients=["aicontentcreator772@gmail.com"],
            body=f"Feedback from: {user_email}\n\nMessage:\n{user_message}",
            reply_to=user_email
        )
        mail.send(msg)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("MAIL ERROR:", e)
        return jsonify({"status": "fail"}), 500
    



@app.route('/send-report', methods=['POST'])
def send_report():
    data = request.get_json()
    user_email = data.get('email')
    user_message = data.get('message')

    # ✅ Save to DB
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('INSERT INTO report (user_email, message) VALUES (?, ?)', (user_email, user_message))
    conn.commit()
    conn.close()

    try:
        msg = Message(
            subject="New Report",
            recipients=["aicontentcreator772@gmail.com"],
            body=f"Report from: {user_email}\n\nMessage:\n{user_message}",
            reply_to=user_email
        )
        mail.send(msg)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("MAIL ERROR:", e)
        return jsonify({"status": "fail"}), 500
    


@app.route('/view_feedback')
def view_feedback():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedbacks = c.fetchall()
    conn.close()
    return render_template('view_feedback.html', feedbacks=feedbacks)

@app.route('/view_reports')
def view_reports():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM report ORDER BY created_at DESC')
    reports = c.fetchall()
    conn.close()
    return render_template('view_reports.html', reports=reports)

@app.route('/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Feedback deleted successfully.', 'success')
    return redirect(url_for('view_feedback'))

@app.route('/delete_report/<int:id>', methods=['POST'])
def delete_report(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM report WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Report deleted successfully.', 'success')
    return redirect(url_for('view_reports'))

# ====================
# RUN
# ====================
from flask import Flask, render_template
import sqlite3
import base64

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8') if data else ''

def get_db_connection():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn


# @app.route('/sellers')
# def show_sellers():
#     if not session.get('seller_logged_in'):
#         return redirect(url_for('login'))  # or your seller login route

#     seller_id = session.get('seller_id')

#     conn = get_db_connection()
#     seller = conn.execute('SELECT * FROM seller_registration WHERE id = ?', (seller_id,)).fetchone()
#     conn.close()

#     if seller:
#         return render_template('sellers.html', sellers=[seller])  # Pass as list
#     else:
#         return "Seller not found", 404










@app.route('/upload_news', methods=['GET', 'POST'])
def upload_news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash("Both title and content are required.")
            return redirect('/upload_news')

        # Get current IST time in 12-hour format with AM/PM
        ist = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(ist)
        formatted_date = now_ist.strftime("%d-%m-%Y %I:%M:%S %p")  # e.g., 28-07-2025 08:06:12 AM

        # Save title, content, and IST timestamp
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute("INSERT INTO news (title, content, date) VALUES (?, ?, ?)", 
                  (title, content, formatted_date))
        conn.commit()
        conn.close()

        flash("News uploaded successfully!")
        return redirect('/upload_news')

    return render_template('upload_news.html')



@app.route('/api/news')
def api_news():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT title, content, date FROM news ORDER BY date DESC")
    news = c.fetchall()
    conn.close()

    news_list = []
    for title, content, date in news:
        try:
            # Convert "YYYY-MM-DD HH:MM:SS" to "DD-MM-YYYY     HH:MM:SS AM/PM"
            dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%d-%m-%Y     %I:%M:%S %p")
        except:
            formatted_date = date  # fallback if already formatted
        news_list.append({
            'title': title,
            'content': content,
            'date': formatted_date
        })

    return jsonify(news_list)




@app.route('/news_list')
def news_list():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT title, content, date FROM news ORDER BY date")
    news = c.fetchall()
    conn.close()
    return render_template("news_list.html", news=news)



@app.route('/manage_news')
def manage_news():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT id, title, content, date FROM news ORDER BY id DESC")
    news_list = [{'id': row[0], 'title': row[1], 'content': row[2], 'date': row[3]} for row in c.fetchall()]
    conn.close()
    return render_template('manage_news.html', news_list=news_list)


@app.route('/api/news', endpoint='fetch_news')
def fetch_all_news():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT id, title, content, date FROM news ORDER BY id DESC')
    news_items = c.fetchall()
    conn.close()
    return jsonify([
        {'id': row[0], 'title': row[1], 'content': row[2], 'date': row[3]}
        for row in news_items
    ])




@app.route('/update_news/<int:id>', methods=['POST'])
def update_news(id):
    try:
        data = request.get_json()
        title = data['title']
        content = data['content']
        updated_date = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')

        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute("UPDATE news SET title = ?, content = ?, date = ? WHERE id = ?", 
                  (title, content, updated_date, id))
        conn.commit()
        conn.close()
        return '', 204
    except Exception as e:
        print("Error updating news:", e)
        return "Error saving news", 500



@app.route('/delete_news/<int:id>')
def delete_news(id):
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute("DELETE FROM news WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return '', 204  # No content
    except Exception as e:
        print("Error deleting news:", e)
        return "Error deleting news", 500



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
