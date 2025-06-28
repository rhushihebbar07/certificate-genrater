def send_certificate_email(name, email, cert_url):
    logo_url = url_for('static', filename='profile_pics/1735566765566.png', _external=True)

    msg = Message(
        subject="🎓 Your Certificate is Ready - SMS College",
        sender=app.config['MAIL_USERNAME'],  # ✅ Explicit sender required for Render
        recipients=[email]
    )

    msg.html = f"""
    <div style='font-family: Arial, sans-serif; max-width:600px; margin:auto;'>
        <h2 style='color:#2563eb;'>Hi {name},</h2>
        <p>🎉 Your project certificate is ready. View or download it below:</p>
        <p><a href="{cert_url}" style="background:#2563eb;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">📄 View Certificate</a></p>
        <br>
        <p>Regards,<br>SMS College</p>
    </div>
    """
    mail.send(msg)
