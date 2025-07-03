from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("role") == "admin" and not session.get("is_superadmin"):
            flash("❌ Admin access only.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function
