from tkinter import messagebox, Tk, Frame, Label, Entry, Button, Text, Scrollbar, Toplevel, END
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from hashlib import sha256
import os
import pickle
import qrcode
import cv2
from pyzbar.pyzbar import decode
from Blockchain import *


# ------------------- LOGIN -------------------
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin":
        messagebox.showinfo("Success", "Login successful")
        login_window.destroy()
        main.deiconify()
    else:
        messagebox.showerror("Error", "Invalid username or password")


def open_login_window():
    global login_window
    login_window = Toplevel(main)
    login_window.title("Login")
    login_window.geometry("300x200")
    login_window.config(bg='lightblue')

    global username_entry, password_entry
    Label(login_window, text="Username:", bg='lightblue').pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)
    Label(login_window, text="Password:", bg='lightblue').pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)
    Button(login_window, text="Login", command=login, bg="white").pack(pady=10)


# ------------------- MAIN WINDOW -------------------
main = Tk()
main.title("Certificate Validation System using Python and Blockchain")
main.geometry("1150x900")
main.configure(bg="lightblue")
main.withdraw()

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()


# ------------------- SAVE CERTIFICATE -------------------
def saveCertificate():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir="certificate_templates")
    if not filename:
        return

    with open(filename, "rb") as f:
        bytes_data = f.read()

    roll_no = tf1.get()
    name = tf2.get()
    contact = tf3.get()
    batch_no = tf4.get()
    passout_year_month = tf5.get()
    auth_certi = tf6.get()

    if all([roll_no, name, contact, batch_no, passout_year_month, auth_certi]):
        digital_signature = sha256(bytes_data).hexdigest()
        data = f"{roll_no}#{name}#{contact}#{digital_signature}#{batch_no}#{passout_year_month}#{auth_certi}"

        blockchain.add_new_transaction(data)
        blockchain.mine()
        b = blockchain.chain[-1]

        text.insert(END, f"Blockchain Previous Hash : {b.previous_hash}\n"
                         f"Block No : {b.index}\nCurrent Hash : {b.hash}\n")
        text.insert(END, f"Certificate Digital Signature : {digital_signature}\n\n")

        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        # ✅ Generate QR Code including full hash
        qr_info = (
            f"Certificate Verification\n"
            f"Roll No: {roll_no}\n"
            f"Name: {name}\n"
            f"Batch: {batch_no}\n"
            f"Hash: {digital_signature}"
        )
        qr_img = qrcode.make(qr_info)
        qr_filename = f"QR_{roll_no}.png"
        qr_img.save(qr_filename)

        text.insert(END, f"QR Code generated and saved as {qr_filename}\n")

        # ✅ Display QR in GUI
        try:
            qr_image = Image.open(qr_filename)
            qr_image = qr_image.resize((180, 180), Image.Resampling.LANCZOS)
            qr_image = ImageTk.PhotoImage(qr_image)
            qr_display.configure(image=qr_image)
            qr_display.image = qr_image
            text.insert(END, "QR code preview displayed successfully.\n")
        except Exception as e:
            text.insert(END, f"Error displaying QR code: {e}\n")

    else:
        text.insert(END, "Please enter all student details\n")


# ------------------- VERIFY CERTIFICATE -------------------
def verifyCertificate():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir="certificate_templates")
    if not filename:
        return

    with open(filename, "rb") as f:
        bytes_data = f.read()

    digital_signature = sha256(bytes_data).hexdigest()
    found = False

    for i in range(1, len(blockchain.chain)):
        b = blockchain.chain[i]
        data = b.transactions[0]
        arr = data.split("#")
        if arr[3] == digital_signature:
            text.insert(END, "Certificate Uploaded\n")
            text.insert(END, "Details extracted from Blockchain after Validation\n\n")
            text.insert(END, f"Digital Sign : {arr[3]}\nRoll No : {arr[0]}\n"
                             f"Student Name : {arr[1]}\nContact No : {arr[2]}\n"
                             f"Batch No : {arr[4]}\nPassed Out Year and Month : {arr[5]}\n"
                             f"Certificate Authorized By : {arr[6]}\n\n")
            found = True
            break

    if not found:
        text.insert(END, "Verification Failed or Certificate Forged\n")


# ------------------- VERIFY QR -------------------
def verifyQR():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir=".", title="Select QR Code Image",
                               filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
    if not filename:
        return

    try:
        img = cv2.imread(filename)
        detected_qr = decode(img)

        if not detected_qr:
            text.insert(END, "No QR code detected or unreadable image.\n")
            return

        for qr in detected_qr:
            qr_data = qr.data.decode('utf-8')
            text.insert(END, "QR Code Scanned Successfully ✅\n\n")
            text.insert(END, "QR Content:\n")
            text.insert(END, f"{qr_data}\n\n")

            # Extract hash for verification
            qr_lines = qr_data.split("\n")
            hash_value = None
            for line in qr_lines:
                if line.startswith("Hash:"):
                    hash_value = line.split(":", 1)[1].strip()
                    break

            if not hash_value:
                text.insert(END, "⚠️ Hash not found in QR data.\n")
                return

            # Cross-check in blockchain
            valid = False
            for i in range(1, len(blockchain.chain)):
                b = blockchain.chain[i]
                if any(hash_value in t for t in b.transactions):
                    valid = True
                    break

            if valid:
                text.insert(END, "✅ QR Verified: Certificate is VALID.\n", 'valid')
            else:
                text.insert(END, "❌ QR Verification Failed: Certificate is FORGED or not in Blockchain.\n", 'invalid')

        text.tag_config('valid', foreground='green', font=('times', 13, 'bold'))
        text.tag_config('invalid', foreground='red', font=('times', 13, 'bold'))

    except Exception as e:
        text.insert(END, f"Error reading QR Code: {e}\n")


# ------------------- GUI DESIGN -------------------
font_title = ('times', 20, 'bold')
font1 = ('times', 13, 'bold')

# ----- TITLE -----
title_frame = Frame(main, bg='lightblue')
title_frame.pack(pady=20)

try:
    logo_image = Image.open('logo.jpg')
    logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
    logo_image = ImageTk.PhotoImage(logo_image)
    logo_label = Label(title_frame, image=logo_image, bg='lightblue')
    logo_label.pack(side='left', padx=15)
except:
    logo_label = None

title_text = Label(title_frame,
                   text="Certificate Verification System\nUsing Python and Blockchain",
                   font=font_title, bg='lightblue', fg='darkblue', justify='center')
title_text.pack(side='left')

# ----- FORM -----
form_frame = Frame(main, bg='lightblue')
form_frame.pack(pady=20)

labels_text = [
    'Roll No :', 'Student Name :', 'Contact No :',
    'Batch No :', 'Passout Year and Month :', 'Certificate Authorized by :'
]

entries = []
for i, text_label in enumerate(labels_text[:3]):
    Label(form_frame, text=text_label, font=font1, bg='lightblue').grid(row=i, column=0, padx=10, pady=10, sticky='e')
    e = Entry(form_frame, width=25, font=font1)
    e.grid(row=i, column=1, padx=10, pady=10)
    entries.append(e)
for i, text_label in enumerate(labels_text[3:]):
    Label(form_frame, text=text_label, font=font1, bg='lightblue').grid(row=i, column=2, padx=10, pady=10, sticky='e')
    e = Entry(form_frame, width=25, font=font1)
    e.grid(row=i, column=3, padx=10, pady=10)
    entries.append(e)

tf1, tf2, tf3, tf4, tf5, tf6 = entries

# ----- BUTTONS -----
button_frame = Frame(main, bg='lightblue')
button_frame.pack(pady=10)

Button(button_frame, text="Save Certificate", command=saveCertificate,
       font=font1, bg='lightgreen', width=18).grid(row=0, column=0, padx=25)
Button(button_frame, text="Verify Certificate", command=verifyCertificate,
       font=font1, bg='mistyrose', width=18).grid(row=0, column=1, padx=25)
Button(button_frame, text="Verify via QR", command=verifyQR,
       font=font1, bg='lightblue', width=18).grid(row=0, column=2, padx=25)

# ----- OUTPUT -----
output_frame = Frame(main, bg='lightblue')
output_frame.pack(pady=30)

text = Text(output_frame, height=18, width=95, font=font1, bg='wheat')
text.grid(row=0, column=0, padx=10, pady=10)

scroll = Scrollbar(output_frame, command=text.yview)
text.configure(yscrollcommand=scroll.set)
scroll.grid(row=0, column=1, sticky='ns')

qr_display = Label(output_frame, bg='lightblue')
qr_display.grid(row=0, column=2, padx=20)

open_login_window()
main.mainloop()
