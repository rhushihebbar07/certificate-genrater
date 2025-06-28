import smtplib
from email.message import EmailMessage

def send_certificate_email(name, recipient_email, cert_url):
    # Setup email message
    msg = EmailMessage()
    msg["Subject"] = "🎓 Your Project Completion Certificate - SMS College"
    msg["From"] = "donotreplay93@gmail.com"
    msg["To"] = recipient_email

    # Email body (text fallback and HTML for Gmail/webmail)
    msg.set_content(f"Hi {name},\n\nYour project has been approved!\nDownload your certificate here: {cert_url}\n\nRegards,\nSMS College")

    html_content = f"""
    <html>
      <body style="font-family: 'Segoe UI', sans-serif; background-color: #f9fafb; padding: 20px; color: #111827;">
        <h2 style="color: #1e3a8a;">🎉 Congratulations, {name}!</h2>
        <p>Your GitHub project has been <strong>approved</strong> by our Department of Computer Applications.</p>
        <p>👉 <a href="{cert_url}" style="color: #2563eb;">Click here to view or download your certificate</a></p>
        <br>
        <p>Best regards,<br><strong>Saint Mary's Syrian College</strong></p>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    # Send email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("donotreplay93@gmail.com", "pnai waam mzpp stjd")
            smtp.send_message(msg)
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
