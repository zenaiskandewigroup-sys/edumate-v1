# 🎓 EduMate v1 — AI Education Assistant  

EduMate is an **AI-powered education platform** that helps students learn smarter and faster using **Gemini API**.  
It combines an AI chatbot, quiz generator, and study assistant — all built into one lightweight, browser-accessible web app.  

---

## 🧩 Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Installation Guide](#installation-guide)  
5. [Running the Application](#running-the-application)  
6. [Testing Instructions (for Devpost)](#testing-instructions-for-devpost)  
7. [Problem & Solution](#problem--solution)  
8. [Author](#author)  
9. [License](#license)  
10. [Bahasa Indonesia](#🇮🇩-versi-bahasa-indonesia)  

---

## 📘 Overview
EduMate is designed for students in developing countries who lack access to interactive and affordable learning tools.  
With Gemini API integration, EduMate answers academic questions, explains topics, and generates quizzes instantly — right from your browser.  

---

## 🚀 Features
- 🤖 **AI Chatbot** — Ask any academic question and get instant, detailed answers powered by **Gemini API**.  
- 🧩 **Quiz Generator** — Automatically creates quizzes from user-selected topics.  
- 📚 **Study Mode** — Structured explanations (History → Definition → Discussion → Example Questions).  
- 🔐 **User Authentication** — Simple login/register system to store progress.  
- 💻 **Responsive Frontend** — Works on mobile, desktop, or even inside Termux browsers.  

---

## 🧰 Tech Stack
| Component | Technology |
|------------|-------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (FastAPI) |
| **Database** | SQLite |
| **AI Integration** | Google Gemini API |
| **Environment** | Termux / Ubuntu / Localhost |

---

## ⚙️ Installation Guide  

### 🪄 1️⃣ Clone the Repository  
Clone this repository to your device (Termux or desktop):
```bash
git clone https://github.com/zenaiskandewigroup-sys/edumate-v1.git
cd edumate-v1


---

🧠 2️⃣ Setup the Virtual Environment (optional but recommended)

python3 -m venv chatbot-env
source chatbot-env/bin/activate


---

📦 3️⃣ Install Dependencies

Move into the backend folder and install all required libraries:

cd backend
pip install -r requirements.txt

If requirements.txt doesn’t exist, install manually:

pip install fastapi uvicorn requests sqlite3


---

🔑 4️⃣ Configure Gemini API Key

Create an API key from Google AI Studio,
then export it as an environment variable:

export GEMINI_API_KEY="YOUR_API_KEY"


---

▶️ Running the Application

🖥 Start Backend Server

Run the FastAPI backend with:

python app.py

If using uvicorn manually:

uvicorn app:app --host 0.0.0.0 --port 8000 --reload

Once started, backend will be live at:
🌐 http://127.0.0.1:8000
You can check if it’s running by opening:

http://127.0.0.1:8000/health


---

🌐 Open the Frontend

In a new terminal window:

cd ~/edumate-v1/frontend

Then open the main HTML page in your browser:

xdg-open index.html

Or manually open it through your browser’s file system:

file:///path/to/edumate-v1/frontend/index.html

✅ Once opened, you’ll see:

A homepage with menu navigation

Chatbot feature connected to Gemini API

Quiz generation and study sections



---

🧪 Testing Instructions for Devpost

Step-by-step:

1. Clone this repository

git clone https://github.com/zenaiskandewigroup-sys/edumate-v1.git
cd edumate-v1


2. Install dependencies

cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_API_KEY"


3. Run the backend

python app.py


4. Open frontend

cd ../frontend
xdg-open index.html


5. Test the app

Ask AI chatbot academic questions

Generate quizzes from a chosen topic

Explore study material mode




The app runs locally — no cloud setup required.


---

💡 Problem & Solution

Problem:
Millions of students in developing countries lack access to interactive, intelligent learning tools.

Solution:
EduMate offers an offline-capable AI tutor, combining learning assistance and auto-generated quizzes powered by Gemini API — designed to run even on low-end devices.


---

🧑‍💻 Author

Zena Iskandewi Group
Built for VirtuHack / Google AI Challenge 2025
📧 Contact: zenaiskandewigroup@gmail.com


---

📜 License

This project is licensed under the MIT License — free for personal and educational use.


---

🇮🇩 Versi Bahasa Indonesia

🎓 EduMate v1 — Asisten Belajar Berbasis AI

EduMate adalah aplikasi EdTech bertenaga AI yang membantu siswa belajar lebih cepat dan interaktif.
Menggunakan Gemini API, EduMate berfungsi sebagai chatbot pembelajaran, generator kuis, dan asisten studi dalam satu platform ringan.


---

🧠 Fitur Utama

🤖 Chatbot AI untuk menjawab dan menjelaskan materi

🧩 Generator kuis otomatis berdasarkan topik

📘 Mode belajar terstruktur (Sejarah → Definisi → Contoh Soal)

🔐 Login pengguna sederhana

🌐 Bisa dijalankan langsung dari HP atau PC



---

⚙️ Langkah Instalasi

git clone https://github.com/zenaiskandewigroup-sys/edumate-v1.git
cd edumate-v1
cd backend
pip install -r requirements.txt
export GEMINI_API_KEY="API_KEY_KAMU"
python app.py

Lalu buka frontend:

cd ../frontend
xdg-open index.html

Atau buka manual:

file:///path/to/edumate-v1/frontend/index.html


---

💡 Masalah & Solusi

Banyak siswa di daerah berkembang tidak memiliki akses ke alat belajar interaktif.
EduMate hadir sebagai solusi AI edukatif ringan yang bisa dijalankan secara lokal — bahkan lewat Termux di HP Android.


---

👨‍💻 Pengembang

Zena Iskandewi Group — dibuat untuk kompetisi Google AI Challenge 2025
Lisensi: MIT License

---

### 💬 Petunjuk:
1. Buka GitHub → buka file `README.md`  
2. Klik tombol ✏️ (edit)  
3. Hapus semua isi lama → **paste isi di atas**  
4. Klik **Commit changes ✅**

Selesai — README lo langsung tampil profesional banget.  
Mau sekalian gue tambahin versi dengan **badge visual (Gemini API, FastAPI, MIT License, dll)** biar makin keren di GitHub repo lo?
