# utils/email_sender.py

import smtplib
from email.message import EmailMessage

def send_certificate_email(name, recipient_email, cert_url):
    msg = EmailMessage()
    msg["Subject"] = "🎓 Your Project Completion Certificate - SMS College"
    msg["From"] = "donotreplay93@gmail.com"  # ✅ Explicit sender required
    msg["To"] = recipient_email

    msg.set_content(f"Hi {name},\n\nYour certificate is ready at: {cert_url}")

    msg.add_alternative(f"""
    <html>
      <body style="font-family: 'Segoe UI', sans-serif; background-color: #f9fafb; padding: 20px; color: #111827;">
        <h2 style="color: #1e3a8a;">🎉 Congratulations, {name}!</h2>
        <p>Your GitHub project has been <strong>approved</strong> by the Department of Computer Applications.</p>
        <p><a href="{cert_url}" style="color: #2563eb; font-weight: bold;">📄 View Your Certificate</a></p>
        <br>
        <p>Best regards,<br><strong>Saint Mary's Syrian College</strong></p>
      </body>
    </html>
    """, subtype='html')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("donotreplay93@gmail.com", "pnai waam mzpp stjd")  # ✅ Use environment variables in production
            smtp.send_message(msg)
            print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Email sending failed for {recipient_email}: {e}")
