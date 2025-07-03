import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

from utils.email_utils import send_certificate_email


def send_certificate_email(name, recipient_email, cert_url):
    sender_email = "donotreplay93@gmail.com"
    sender_password = "pnai waam mzpp stjd"

    # 🔐 Safe sender with display name
    sender_name = "XYZ College Certificates 🎓"
    formatted_sender = formataddr((str(Header(sender_name, 'utf-8')), sender_email))

    # Create the multipart message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = str(Header("🎓 Your Project Completion Certificate", "utf-8"))
    msg["From"] = formatted_sender
    msg["To"] = recipient_email

    # 📄 Text fallback version
    text_content = f"""
Hi {name},

Congratulations! Your GitHub project has been approved.

Your certificate is ready. View or download it here:
{cert_url}

— XYZ College Certificate System
    """

    # 🖼️ HTML version
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px;">
          <h2>Hi {name},</h2>
          <p>🎉 Congratulations! Your GitHub project has been approved by <strong>XYZ College</strong>.</p>
          <p>Your certificate is ready. Click the button below to view or download it:</p>
          <p style="text-align: center;">
            <a href="{cert_url}" style="display: inline-block; background-color: #4CAF50; color: white;
               padding: 12px 24px; text-decoration: none; border-radius: 6px; font-size: 16px;">
              📄 View Certificate
            </a>
          </p>
          <p>If the button doesn't work, copy and paste this link:</p>
          <p><a href="{cert_url}">{cert_url}</a></p>
          <hr />
          <p style="font-size: 12px; color: #999;">This is an automated email from the SMS College Certificate System.</p>
        </div>
      </body>
    </html>
    """

    # Attach both plain text and HTML
    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Email sending failed:", e)
        raise
