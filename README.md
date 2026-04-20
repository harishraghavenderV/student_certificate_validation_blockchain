# 🎓 Student Certificate Validation using Python & Blockchain

## 🔍 Overview
A secure certificate verification system that prevents forgery by combining blockchain-based storage with SHA-256 hashing and QR-based validation.

Each certificate is uniquely hashed and stored in a custom blockchain structure, ensuring immutability and tamper detection.

---

## ⚙️ Key Features
- 🔐 Admin login for secure certificate management  
- 🧾 SHA-256 hashing for certificate integrity  
- ⛓️ Custom blockchain implementation for tamper-proof storage  
- 🖼️ QR code generation for each certificate  
- 📱 QR-based verification using OpenCV and Pyzbar  
- ✅ Instant validation result: **VALID / FORGED**

---

## 🧠 System Workflow
1. Certificate details are entered via GUI  
2. Data is converted into a SHA-256 hash  
3. Hash is stored inside a blockchain block  
4. QR code is generated containing certificate reference  
5. During verification:
   - QR code is scanned  
   - Hash is recomputed  
   - Compared with blockchain data  
   - Result displayed as VALID or FORGED  

---

## 🛠️ Tech Stack
| Component | Technology |
|----------|-----------|
| GUI | Tkinter |
| Blockchain | Custom Python Classes |
| Hashing | hashlib (SHA-256) |
| Image Handling | Pillow (PIL) |
| QR Generation | qrcode |
| QR Verification | OpenCV, pyzbar |

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/harishraghavenderV/student_certificate_validation_blockchain.git
cd student_certificate_validation_blockchain
