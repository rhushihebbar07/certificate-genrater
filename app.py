import os
import uuid
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, send_file
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from weasyprint import HTML
from decorators import admin_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'

from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file

app.secret_key = os.getenv("SECRET_KEY", "fallbacksecretkey")


app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

os.makedirs("certs", exist_ok=True)
os.makedirs("static/profile_pics", exist_ok=True)
os.makedirs("database", exist_ok=True)
DATABASE = "database/users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def set_session_behavior():
    session.permanent = False

@app.route("/")
def root_redirect():
    if "user_id" not in session:
        session.clear()
        return redirect(url_for("login"))
    return redirect(url_for("admin_dashboard" if session.get("is_admin") else "dashboard"))

from datetime import datetime
from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and user["password"] == password:
            session.clear()
            session.update({
                "user_id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "profile_pic": user["profile_pic"] or "default.png",
                "role": user["role"] if "role" in user.keys() else "student",
                "is_admin": user["role"] == "admin" if "role" in user.keys() else False,
                "is_superadmin": user["is_superadmin"] == 1 if "is_superadmin" in user.keys() else False,
                "view_as_admin": user["role"] == "admin" if "role" in user.keys() else False,
                "just_logged_in": True
            })

            flash(f"✅ Welcome back, {user['username']}!", "success")

            if session["is_admin"] or session["is_superadmin"]:
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))

        flash("❌ Invalid email or password", "error")

    return render_template("login.html")


def send_certificate_email(name, email, cert_url):
    logo_url = "static/profile_pics/1735566765566.png"  # 🔁 replace with your logo
    banner_url = "https://yourdomain.com/static/certificate_banner.png"  # 🔁 optional banner
    signature_url = "https://yourdomain.com/static/principal_sign.png"  # 🔁 optional signature

    msg = Message(
        subject="🎓 Your Certificate is Ready - XYZ College",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.html = f"""
    <div style="font-family: 'Segoe UI', sans-serif; color: #1e293b; max-width: 600px; margin: auto; border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden;">
        <div style="padding: 20px; text-align: center; background-color: #f8fafc;">
            <img src="{logo_url}" alt="XYZ College Logo" style="max-height: 80px; margin-bottom: 10px;">
            <h2 style="color: #2563eb; margin: 0;">Saint Mary's Syrian College</h2>
            <p style="margin: 0; font-weight: 500;">Department of Computer Applications</p>
        </div>

        <div style="padding: 30px; background-color: #ffffff;">
            <img src="{banner_url}" alt="Certificate Banner" style="width: 100%; border-radius: 10px; margin-bottom: 20px;">

            <h3 style="color: #0f172a;">🎉 Congratulations, {name}!</h3>
            <p style="font-size: 16px;">Your GitHub project has been <strong>successfully approved</strong> by our team.</p>
            <p style="font-size: 15px;">You can now download or view your official certificate using the button below.</p>

            <div style="text-align: center; margin: 25px 0;">
                <a href="{cert_url}" target="_blank" style="background-color: #2563eb; color: #ffffff; padding: 14px 30px; font-size: 16px; text-decoration: none; border-radius: 8px; font-weight: bold;">📄 View Certificate</a>
            </div>

            <p style="font-size: 15px; color: #334155;">If you face any issues, feel free to contact our department.</p>

            <div style="margin-top: 30px;">
                <img src="{signature_url}" alt="Principal Signature" style="height: 60px;"><br>
                <p style="font-size: 14px; margin-top: 5px;">Principal<br>XYZ College</p>
            </div>
        </div>

        <div style="padding: 20px; text-align: center; font-size: 13px; background-color: #f1f5f9; color: #64748b;">
            &copy; 2025 Saint Mary's Syrian College · All rights reserved<br>
            <a href="https://smscollege.edu" style="color: #2563eb; text-decoration: none;">smscollege.edu</a>
        </div>
    </div>
    """
    mail.send(msg)



@app.route("/admin/export-users")
def export_users():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    df = pd.DataFrame(users)
    filename = "exported_users.xlsx"
    filepath = os.path.join("certs", filename)
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

@app.route("/admin/export-projects")
def export_projects():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    projects = conn.execute('''SELECT p.*, u.username, u.email FROM projects p JOIN users u ON p.user_id = u.id''').fetchall()
    conn.close()
    df = pd.DataFrame(projects)
    filename = "exported_projects.xlsx"
    filepath = os.path.join("certs", filename)
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user:
            token = serializer.dumps(email, salt='reset-password')
            reset_url = url_for('reset_password', token=token, _external=True)
            msg = Message("🔐 Reset Your Password - XYZ College", sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.html = f"""<div style='font-family: Arial, sans-serif;'>
                <h2>🔐 Password Reset Request</h2>
                <p>Hi {user['first_name']}, click below to reset your password:</p>
                <p><a href="{reset_url}" style="padding:10px 20px;background:#2d6cdf;color:#fff;text-decoration:none;">Reset Password</a></p>
                <p>Ignore if you didn't request.</p><p>Link valid for 15 minutes.</p></div>"""
            mail.send(msg)
            flash("✅ Reset link sent to your email.", "success")
        else:
            flash("Email not found.", "error")
    return render_template("forgot_password.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=900)
    except:
        return "❌ Link expired or invalid.", 400
    if request.method == "POST":
        if request.form["password"] != request.form["confirm"]:
            flash("Passwords do not match.", "error")
            return redirect(request.url)
        conn = get_db_connection()
        conn.execute("UPDATE users SET password = ? WHERE email = ?", (request.form["password"], email))
        conn.commit()
        conn.close()
        flash("✅ Password updated! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html")
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM projects WHERE user_id = ?", (session["user_id"],)).fetchone()

    if request.method == "POST":
        if existing:
            flash("❌ You can only upload one project.", "error")
            return redirect(url_for("dashboard"))

        conn.execute('''INSERT INTO projects (user_id, github_url, project_title, is_approved, submitted_on)
                        VALUES (?, ?, ?, 0, ?)''',
                     (session["user_id"], request.form["github_url"],
                      request.form.get("project_title", "").strip() or "Untitled Project",
                      datetime.now().strftime("%d %B %Y")))
        conn.commit()
        conn.close()

        session["uploaded_project"] = True  # ✅ valid place to set it
        flash("✅ Project submitted for approval.", "success")
        return redirect(url_for("dashboard"))

    conn.close()
    return render_template("index.html", existing_project=existing)




@app.route("/dashboard/reset", methods=["POST"])
def reset_project():
    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))

    admin_pass = request.form.get("admin_password")
    # Only allow reset if admin password correct
    if admin_pass != "smsbcabvr":
        flash("❌ Incorrect admin password.", "error")
        return redirect(url_for("dashboard"))

    # If admin, allow reset for any user_id (passed optionally)
    user_id_to_reset = request.form.get("user_id")
    if not user_id_to_reset:
        # If no user_id specified, reset own project
        user_id_to_reset = session["user_id"]
    else:
        # Only admin can reset others projects
        if not session.get("is_admin"):
            flash("❌ Unauthorized to reset others' projects.", "error")
            return redirect(url_for("dashboard"))

    conn = get_db_connection()
    conn.execute("DELETE FROM projects WHERE user_id = ?", (user_id_to_reset,))
    conn.commit()
    conn.close()
    flash("✅ Project submission has been reset.", "success")
    return redirect(url_for("dashboard") if user_id_to_reset == session["user_id"] else url_for("admin_dashboard"))

# NEW: Bulk reset all projects route for admin
@app.route("/admin/reset-all-projects", methods=["POST"])
def reset_all_projects():
    if not session.get("is_admin"):
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))
    
    admin_pass = request.form.get("admin_password_all")
    if admin_pass != "smsbcabvr":
        flash("❌ Incorrect admin password for bulk reset.", "error")
        return redirect(url_for("admin_dashboard"))
    
    conn = get_db_connection()
    conn.execute("DELETE FROM projects")
    conn.commit()
    conn.close()

    flash("✅ All project submissions have been reset.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin")
def admin_dashboard():
    # Allow only superadmin, admin, or lecturer
    if not (session.get("is_superadmin") or session.get("role") in ["admin", "lecturer"]):
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()

    # Fetch all users (only for admin/superadmin)
    if session.get("is_superadmin") or session.get("role") == "admin":
        users = conn.execute("SELECT * FROM users").fetchall()
    else:
        users = []

    # Get all projects
    projects = conn.execute('''
        SELECT p.*, u.username, u.email 
        FROM projects p 
        JOIN users u ON p.user_id = u.id
    ''').fetchall()

    # Certificate stats
    approved_count = conn.execute("SELECT COUNT(*) FROM projects WHERE is_approved = 1").fetchone()[0]
    pending_count = conn.execute("SELECT COUNT(*) FROM projects WHERE is_approved = 0").fetchone()[0]

    # Get recent user login activity
    recent_threshold = datetime.utcnow() - timedelta(minutes=10)
    logins = conn.execute("SELECT user_id, MAX(timestamp) AS last_seen FROM login_logs GROUP BY user_id").fetchall()

    online_user_ids = set()
    user_last_seen = {}

    for log in logins:
        last_seen = datetime.strptime(log["last_seen"], "%Y-%m-%d %H:%M:%S")
        user_last_seen[log["user_id"]] = last_seen
        if last_seen >= recent_threshold:
            online_user_ids.add(log["user_id"])

    all_users = []
    for u in users:
        user_dict = dict(u)
        user_dict["is_online"] = u["id"] in online_user_ids
        user_dict["last_seen"] = user_last_seen.get(u["id"], None)
        all_users.append(user_dict)

    conn.close()

    return render_template("admin_dashboard.html",
                           users=users,
                           projects=projects,
                           approved_count=approved_count,
                           pending_count=pending_count,
                           all_users=all_users)

import requests

def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("⚠️ Could not fetch ngrok URL:", e)
        return None


import requests

def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("⚠️ Could not fetch ngrok URL:", e)
        return None


@app.route("/admin/approve-project/<int:project_id>")
def approve_project(project_id):
    if not (session.get("is_superadmin") or session.get("role") in ["admin", "lecturer"]):
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    project = conn.execute('''SELECT p.*, u.first_name, u.email
                              FROM projects p JOIN users u ON p.user_id = u.id
                              WHERE p.id = ?''', (project_id,)).fetchone()
    if not project:
        conn.close()
        return "Project not found", 404

    cert_id = str(uuid.uuid4())[:8]
    cert_filename = f"{cert_id}.pdf"
    cert_path = os.path.join("certs", cert_filename)

    # 🔁 Dynamically get ngrok URL
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        cert_url = f"{ngrok_url}/certs/{cert_filename}"
    else:
        cert_url = f"http://localhost:5000/certs/{cert_filename}"  # fallback

    # ✅ Generate certificate
    rendered = render_template("certificate.html", name=project["first_name"],
                               repo_title=project["project_title"],
                               github_url=project["github_url"],
                               date=datetime.now().strftime("%d %B %Y"))
    HTML(string=rendered, base_url='.').write_pdf(cert_path)

    # ✅ Send email only if not a lecturer (optional logic)
    if session.get("role") != "lecturer":
        send_certificate_email(project["first_name"], project["email"], cert_url)

    # ✅ Save approval
    conn.execute("UPDATE projects SET is_approved = 1, cert_file = ? WHERE id = ?", (cert_filename, project_id))
    conn.commit()
    conn.close()

    flash("✅ Project approved and certificate generated.", "success")

    # 🔁 Redirect to correct dashboard
    if session.get("role") == "lecturer":
        return redirect(url_for("lecturer_dashboard"))
    else:
        return redirect(url_for("admin_dashboard"))

@app.route("/lecturer")
def lecturer_dashboard():
    if session.get("role") != "lecturer":
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    projects = conn.execute('''
        SELECT p.*, u.username, u.email 
        FROM projects p 
        JOIN users u ON p.user_id = u.id 
        WHERE p.is_approved = 0
    ''').fetchall()
    conn.close()

    return render_template("lecturer_dashboard.html", projects=projects)

import requests

def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("⚠️ Could not fetch ngrok URL:", e)
        return None


@app.route("/lecturer/approve-project/<int:project_id>", methods=["POST", "GET"])
def lecturer_approve_project(project_id):
    if session.get("role") != "lecturer":
        flash("❌ Unauthorized access.", "danger")
        return redirect(url_for("login"))

    conn = get_db_connection()
    project = conn.execute('''SELECT p.*, u.first_name, u.email
                              FROM projects p JOIN users u ON p.user_id = u.id
                              WHERE p.id = ?''', (project_id,)).fetchone()

    if not project:
        conn.close()
        flash("❌ Project not found.", "error")
        return redirect(url_for("lecturer_dashboard"))

    # Generate unique certificate file
    cert_id = str(uuid.uuid4())[:8]
    cert_filename = f"{cert_id}.pdf"
    cert_path = os.path.join("certs", cert_filename)

    # Get dynamic ngrok URL
    ngrok_url = get_ngrok_url()
    cert_url = f"{ngrok_url}/certs/{cert_filename}" if ngrok_url else f"http://localhost:5000/certs/{cert_filename}"

    # Render and generate PDF certificate
    rendered = render_template("certificate.html",
                               name=project["first_name"],
                               repo_title=project["project_title"],
                               github_url=project["github_url"],
                               date=datetime.now().strftime("%d %B %Y"))
    HTML(string=rendered, base_url='.').write_pdf(cert_path)

    # Send email
    send_certificate_email(project["first_name"], project["email"], cert_url)

    # Mark project as approved
    conn.execute("UPDATE projects SET is_approved = 1, cert_file = ? WHERE id = ?", (cert_filename, project_id))
    conn.commit()
    conn.close()

    flash("✅ Project approved and certificate sent.", "success")
    return redirect(url_for("lecturer_dashboard"))


from flask import send_from_directory, abort
import os

@app.route("/admin/download-profile-pic/<filename>")
def download_profile_pic(filename):
    if not session.get("is_superadmin"):
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    # Define the folder where profile pics are stored
    profile_pics_dir = os.path.join(app.root_path, 'static', 'profile_pics')

    # Security check to prevent directory traversal attacks
    if '..' in filename or filename.startswith('/'):
        abort(400)

    # Check if file exists
    file_path = os.path.join(profile_pics_dir, filename)
    if not os.path.exists(file_path):
        flash("❌ Profile picture not found.", "error")
        return redirect(url_for("admin_user_details", user_id=session.get("user_id")))

    # Send the file for download
    return send_from_directory(profile_pics_dir, filename, as_attachment=True)


@app.route("/admin/user/<int:user_id>", methods=["GET", "POST"])
def admin_user_details(user_id):
    if not session.get("is_admin"): return redirect(url_for("login"))
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user: return "User not found", 404
    if request.method == "POST":
        form = request.form
        conn.execute("""UPDATE users SET
            first_name=?, last_name=?, username=?, email=?, phone=?, age=?,
            class_batch=?, password=?, is_admin=? WHERE id=?""",
            (form["first_name"], form["last_name"], form["username"], form["email"],
             form["phone"], form["age"], form["class_batch"], form["password"],
             int(form.get("is_admin", 0)), user_id))
        conn.commit()
        flash("✅ User updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin_user_edit.html", user=user)

@app.route("/view-certificate")
def view_certificate():
    cert_file = request.args.get("com")
    return render_template("certificate_viewer.html", cert_file=cert_file) if cert_file else "❌ Invalid certificate link", 404

@app.route("/certs/<filename>")
def serve_certificate(filename):
    return send_from_directory("certs", filename)

@app.route("/logout")
def logout():
    session["just_logged_out"] = True  # ✅ Safe here
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))



@app.route("/toggle-role-view")
def toggle_role_view():
    if "user_id" not in session: return redirect(url_for("login"))
    if not session.get("is_admin"): return redirect(url_for("dashboard"))
    session["view_as_admin"] = not session.get("view_as_admin", True)
    flash("Switched to Admin View." if session["view_as_admin"] else "Switched to User View.", "success")
    return redirect(url_for("admin_dashboard" if session["view_as_admin"] else "dashboard"))

@app.route("/admin/make-admin/<int:user_id>")
def make_admin(user_id):
    if not session.get("is_admin"): return redirect(url_for("login"))
    conn = get_db_connection()
    conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (user_id,))
    conn.commit()
    flash("✅ User has been granted admin access.", "success")
    return redirect(url_for("admin_dashboard"))

from werkzeug.utils import secure_filename

from werkzeug.utils import secure_filename
import os
import sqlite3

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        file = request.files.get("profile_pic")
        profile_pic_filename = ""

        # Save profile picture if uploaded
        if file and file.filename:
            profile_pic_filename = secure_filename(file.filename)
            file.save(os.path.join("static/profile_pics", profile_pic_filename))

        # Clean and fetch form data
        email = form["email"].strip().lower()
        username = form["username"].strip()
        password = form["password"]
        confirm = form["confirm"]
        first_name = form["first_name"]
        last_name = form["last_name"]
        phone = form["phone"]
        age = form["age"]
        class_batch = form["class_batch"]
        role = "student"  # ✅ Default role

        # Password match check
        if password != confirm:
            flash("❌ Passwords do not match.", "error")
            return redirect(url_for("register"))

        # Insert into DB
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO users 
                (first_name, last_name, username, email, phone, age, class_batch, profile_pic, password, role)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, username, email, phone, age, class_batch, profile_pic_filename, password, role))
            conn.commit()
            flash("✅ Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("❌ Email already registered.", "error")
            return redirect(url_for("register"))
        finally:
            conn.close()

    return render_template("register.html")

@app.route("/admin/change-role/<int:user_id>", methods=["POST"])
def change_role(user_id):
    if not session.get("is_superadmin"):
        flash("❌ Only Super Admin can change user roles.", "danger")
        return redirect(url_for("login"))

    new_role = request.form.get("role")
    if new_role not in ["student", "lecturer", "admin"]:
        flash("❌ Invalid role specified.", "error")
        return redirect(url_for("admin_dashboard"))

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if not user:
        flash("❌ User not found.", "error")
        conn.close()
        return redirect(url_for("admin_dashboard"))

    # ❗ Fix here: No .get() on sqlite3.Row
    if user["is_superadmin"] == 1:
        flash("❌ Cannot change the role of the Super Admin.", "error")
        conn.close()
        return redirect(url_for("admin_dashboard"))

    if user["id"] == session.get("user_id"):
        flash("❌ You cannot change your own role.", "error")
        conn.close()
        return redirect(url_for("admin_dashboard"))

    conn.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()

    flash(f"✅ Role updated to {new_role.title()}.", "success")
    return redirect(url_for("admin_dashboard"))



@app.route("/admin/revoke-admin/<int:user_id>")
def revoke_admin(user_id):
    if not session.get("is_admin"): return redirect(url_for("login"))
    conn = get_db_connection()
    conn.execute("UPDATE users SET is_admin = 0 WHERE id = ?", (user_id,))
    conn.commit()
    flash("✅ Admin access revoked for the user.", "success")
    return redirect(url_for("admin_dashboard"))

def init_admin():
    conn = get_db_connection()

    # Create tables
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT, last_name TEXT, username TEXT,
        email TEXT UNIQUE, phone TEXT, age INTEGER,
        class_batch TEXT, profile_pic TEXT,
        password TEXT, is_admin INTEGER DEFAULT 0
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        github_url TEXT,
        project_title TEXT,
        cert_file TEXT,
        submitted_on TEXT,
        is_approved INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS login_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT,
        ip TEXT,
        user_agent TEXT,
        location TEXT,
        login_time TEXT,
        logout_time TEXT
    )''')

    # Alter table only if needed
    try:
        conn.execute("ALTER TABLE login_logs ADD COLUMN timestamp TEXT")
    except sqlite3.OperationalError:
        pass  # Already exists

    # Create default admin if not exists
    admin = conn.execute("SELECT * FROM users WHERE email = 'admin@smscollege.edu'").fetchone()
    if not admin:
        conn.execute('''INSERT INTO users (
            first_name, last_name, username, email, phone,
            age, class_batch, profile_pic, password, is_admin
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)''', (
            "Admin", "Account", "admin", "admin@smscollege.edu",
            "0000000000", 0, "Admin", "", "smsbcabvr"
        ))
        print("[INFO] Default admin created.")
        conn.commit()

    conn.close()
    print("[INFO] Database initialized successfully.")

    
@app.route("/profile")
def user_profile():
    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()

    if not user:
        return "User not found", 404

    return render_template("user_profile.html", user=user)

from flask import send_from_directory, abort

@app.route('/user/profile_pic/<filename>')
def user_profile_pic(filename):
    if "user_id" not in session:
        abort(403)
    return send_from_directory('private/profile_pics', filename)


@app.route("/admin/delete-user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    # Only allow superadmins or admins to delete users
    if not session.get("is_superadmin") and session.get("role") != "admin":
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    # Prevent deletion if user is superadmin
    if user and user["is_superadmin"] == 1:
        flash("❌ Cannot delete the Super Admin.", "error")
        conn.close()
        return redirect(url_for("admin_dashboard"))

    # Prevent deletion of other admins if current user is not superadmin
    if user and user["role"] == "admin" and not session.get("is_superadmin"):
        flash("❌ Cannot delete another admin unless you are Super Admin.", "error")
        conn.close()
        return redirect(url_for("admin_dashboard"))

    # Delete user and related projects
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.execute("DELETE FROM projects WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    flash("✅ User and their projects deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete-all-non-admins", methods=["POST"])
def delete_all_non_admins():
    if not session.get("is_superadmin") and session.get("role") != "admin":
        flash("❌ Unauthorized access.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()

    # Delete only users who are NOT admins or superadmins
    conn.execute("""
        DELETE FROM users 
        WHERE role != 'admin' AND IFNULL(is_superadmin, 0) = 0
    """)

    # Clean up orphaned projects
    conn.execute("""
        DELETE FROM projects 
        WHERE user_id NOT IN (SELECT id FROM users)
    """)

    conn.commit()
    conn.close()

    flash("✅ All non-admin users and their projects have been deleted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/analyze-project/<int:project_id>")
def analyze_project(project_id):
    if not session.get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()

    if not project:
        return jsonify({"error": "Project not found"}), 404

    github_url = project["github_url"]
    try:
        parts = github_url.strip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url)
        repo_data = response.json()

        # Get language breakdown
        lang_data = requests.get(f"{api_url}/languages").json()

        return jsonify({
            "name": repo_data.get("name"),
            "description": repo_data.get("description"),
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "language": repo_data.get("language"),
            "languages": lang_data,
            "last_updated": repo_data.get("updated_at"),
            "html_url": repo_data.get("html_url")
        })
    except Exception as e:
        return jsonify({"error": "Failed to fetch GitHub data."}), 500
    
@app.route("/admin/login-logs", endpoint='view_login_logs')
def view_login_logs():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM login_logs").fetchall()
    conn.close()
    df = pd.DataFrame(logs)
    filepath = os.path.join("certs", "login_logs.xlsx")
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)


@app.route("/admin/export-login-logs")
def export_login_logs():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM login_logs").fetchall()
    conn.close()
    df = pd.DataFrame(logs)
    filepath = os.path.join("certs", "login_logs.xlsx")
    df.to_excel(filepath, index=False)
    return send_file(filepath, as_attachment=True)

@app.route("/admin/user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if not session.get("is_superadmin") and session.get("role") != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("login"))

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if not user:
        conn.close()
        flash("User not found", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        class_batch = request.form["class_batch"]
        role = request.form["role"]  # 👈 capture new role

        conn.execute('''
            UPDATE users
            SET first_name = ?, last_name = ?, email = ?, phone = ?, class_batch = ?, role = ?
            WHERE id = ?
        ''', (first_name, last_name, email, phone, class_batch, role, user_id))

        conn.commit()
        conn.close()

        flash("✅ User details updated.", "success")
        return redirect(url_for("admin_dashboard"))

    conn.close()
    return render_template("edit_user.html", user=user)



if __name__ == "__main__":
    init_admin()
    app.run(debug=True)
