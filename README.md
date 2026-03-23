# 🚀 Server Health Monitor

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

A **real-time Server Health Monitoring Tool** that tracks system performance metrics such as CPU usage, memory utilization, disk space, and network activity. The system sends **instant alerts via Telegram and Email** when thresholds are exceeded.

---

## 📌 Features

* 📊 Real-time monitoring of:

  * CPU Usage
  * Memory Usage
  * Disk Space
  * Network Activity
* 🚨 Instant alerts via:

  * Telegram Bot
  * Email Notifications
* 🔐 Remote server monitoring using SSH
* 🖥️ Simple and user-friendly interface
* ⚡ Lightweight and efficient

---

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:**

  * psutil
  * paramiko
  * smtplib
* **Tools & APIs:**

  * Telegram Bot API
  * Tkinter / PyQt (GUI)

---

## 📂 Project Structure

```
Server_Health_Monitor/
│
├── main.py
├── monitor.py
├── alert.py
├── config.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/amitkumar2/Server_Health_Monitor.git
cd Server_Health_Monitor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

---

## 🔔 Alert Configuration

### Telegram Setup

1. Open Telegram and search **BotFather**
2. Create a new bot
3. Copy the **Bot Token**
4. Get your **Chat ID**
5. Paste them in `config.py`

### Email Setup

* Add your email & password in `config.py`
* Enable **App Passwords** (recommended for Gmail)

---

## 🎯 Future Improvements

* 🌐 Web dashboard (Flask / Django)
* ☁️ Cloud monitoring (AWS / Azure)
* 📈 Graphs & analytics dashboard
* 🤖 AI-based anomaly detection

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork and submit a PR.

---

## 👨‍💻 Author

**Amit Kumar**
GitHub: https://github.com/amitkumar2

---

## ⭐ Support

If you like this project, don’t forget to give it a ⭐ on GitHub!
