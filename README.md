# 🎓 Student Certificate Validation using Python and Blockchain

## 🔍 Overview
A secure certificate verification system built using **Python**, **Tkinter**, and **Blockchain**, enhanced with **QR code generation and verification**.

Each certificate is hashed using **SHA-256** and stored on a local blockchain for tamper-proof validation.  
The system generates a unique QR code for every certificate, allowing instant authenticity checks.

---

## ⚙️ Features
- 🔐 Admin Login System  
- 🧾 Certificate Hashing using SHA-256  
- ⛓️ Blockchain for Secure Record Storage  
- 🖼️ QR Code Generation for Each Certificate  
- 📱 QR Verification (Decodes & Cross-checks Blockchain)  
- ✅ Instant “VALID / FORGED” Verification Result  

---

## 🛠️ Tech Stack
| Component | Technology |
|------------|-------------|
| GUI | Tkinter |
| Blockchain | Custom Python Classes |
| Hashing | hashlib (SHA-256) |
| Image Handling | Pillow (PIL) |
| QR Generation | qrcode |
| QR Verification | opencv-python, pyzbar |

---

## 🚀 Run Locally

### 1️⃣ Clone the repo
```bash
git clone https://github.com/harishraghavenderV/student_certificate_validation_blockchain.git
cd student_certificate_validation_blockchain

2️⃣ Install dependencies
pip install pillow qrcode opencv-python pyzbar

3️⃣ Run the app
python main.py


