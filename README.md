<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=F76647&width=435&lines=Welcome+to+Certificate+Generator+🎓;Upload+GitHub+Projects+%F0%9F%93%81;Auto-Certify+via+SMTP+%E2%9C%85;Built+with+Help+from+ChatGPT+%E2%9D%A4%EF%B8%8F" alt="Typing SVG" />
</p>

<h1 align="center">🎓 Certificate Generator Web App</h1>

<p align="center">
  A powerful web app where students can upload their GitHub projects, get them reviewed, and receive a verified certificate via email — with complete role-based access and automated certificate delivery.
</p>

<p align="center">
  <img src="https://img.shields.io/github/repo-size/rhushihebbar07/certificate-genrater?style=flat-square">
  <img src="https://img.shields.io/github/last-commit/rhushihebbar07/certificate-genrater?style=flat-square">
  <img src="https://img.shields.io/badge/Made%20With-Flask-blue?style=flat-square">
  <img src="https://img.shields.io/badge/SMTP-Enabled-green?style=flat-square">
  <img src="https://img.shields.io/badge/Built%20with-ChatGPT-ff69b4?style=flat-square">
</p>

---

## 🚀 Project Overview

- 🔗 Upload GitHub project link
- 👥 Four powerful user roles with custom dashboards
- 📨 Auto-generate & send certificates using SMTP
- 🔐 Secure login, clean interface, and role access control
- ⚡ Smart development workflow built with guidance from **ChatGPT**

---

## 🧩 User Roles

| Role          | Permissions                                                           |
|---------------|------------------------------------------------------------------------|
| 👨‍🎓 **Student**     | Default role — uploads project link                                 |
| 👩‍🏫 **Lecturer**    | Reviews & approves projects via dashboard                           |
| 🛠️ **Admin**        | Can approve projects, view/edit registered users, manage dashboard |
| 🧑‍💼 **Super Admin** | Assigns roles (Lecturer/Admin), oversees entire application         |

---

## 📤 Certificate Approval Workflow

```mermaid
graph TD
A[Student Uploads GitHub Project] --> B[Lecturer/Admin Reviews]
B --> C[On Approval, Certificate is Generated]
C --> D[Certificate is Sent via SMTP to Student]

🛠️ Built With
🐍 Python + Flask

💾 SQLite3 Database

🎨 HTML5, CSS3, Bootstrap

✉️ Flask-Mail (SMTP Emailing)

📦 certificate-genrater/
├── static/
│   └── profile_pics/       # ⛔ Ignored in repo
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── certificate.html
├── app.py                  # 🔥 Main Flask App
├── database.db             # 📦 SQLite DB (local only)
├── .env                    # 🔐 Hidden credentials
└── README.md               # 📖 This file

🔐 Security
.env and profile_pics/ are hidden via .gitignore

SMTP credentials are securely stored

Only authorized roles can approve or modify data

🧠 ChatGPT Involvement
This project was developed with assistance and code-generation support from ChatGPT for:

Designing clean Flask routes and templates

Handling user role logic

Crafting the SMTP certificate delivery system

Writing this stylish, professional README.md 🎉
📫 Author
Rhushi Hebbar
📧 rhushihebbar22@gmail.com
🔗 GitHub Profile

⚡ Future Enhancements
🌐 Deploy to Render/Heroku

📥 Certificate archive history

📊 Analytics dashboard for admin

🎓 College-wide team collaboration & leaderboard

📝 License
Licensed under the MIT License.

© 2025 Rhushi Hebbar. All rights reserved.
