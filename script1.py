import pyqrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import webbrowser
import re

def gerar_qr():
    link = link_entry.get().strip()

    if not link:
        messagebox.showwarning("Campo vazio", "Por favor, insira uma URL.")
        return

    if not re.match(r'^https?://[^\s]+$', link):
        messagebox.showerror("URL inválida", "Insira uma URL válida que comece com http:// ou https://")
        return

    try:
        qr = pyqrcode.create(link)
        qr.png("temp_qr.png", scale=10)
        img = Image.open("temp_qr.png").convert("RGB")
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        img.save("QRCode.png")

        global img_tk
        img_tk = ImageTk.PhotoImage(img)
        img_label.config(image=img_tk)
        status_label.config(text="QR Code gerado com sucesso!", fg="green")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o QR Code:\n{str(e)}")

def compartilhar():
    numero = numero_entry.get().strip()
    link = link_entry.get().strip()

    if not re.match(r'^\+\d{10,15}$', numero):
        messagebox.showerror("Número inválido", "Insira o número no formato +55XXXXXXXXXXX")
        return

    if not link or not re.match(r'^https?://[^\s]+$', link):
        messagebox.showwarning("URL inválida", "Gere um QR Code com uma URL válida antes de compartilhar.")
        return

    whatsapp_link = f"https://wa.me/{numero[1:]}?text={link}"
    webbrowser.open(whatsapp_link)
    status_label.config(text="Abrindo WhatsApp Web...", fg="blue")
    numero_entry.delete(0, tk.END)

janela = tk.Tk()
janela.title("QR & WhatsApp Generator")
janela.configure(bg="#f0f0f0")
janela.resizable(False, False)

tk.Label(janela,
         text="Insira a URL para gerar QR Code:",
         bg="#f0f0f0",
         font=("Arial", 10),
         justify="center").pack(padx=10, pady=(10, 0), anchor="center")
link_entry = tk.Entry(janela, width=50)
link_entry.insert(0, "https://")
link_entry.pack(padx=10, pady=(0,10))

tk.Button(janela,
          text="Gerar QR Code",
          fg="white",
          bg="#00796B",
          font=("Arial", 10, "bold"),
          relief="ridge",
          bd=3,
          command=gerar_qr).pack(pady=(0,10))

img_placeholder = Image.new("RGB", (300,300), "#ffffff")
img_tk = ImageTk.PhotoImage(img_placeholder)
img_label = tk.Label(janela, image=img_tk, bg="#f0f0f0")
img_label.pack(padx=10, pady=10)

tk.Label(janela,
         text="Número do WhatsApp (ex: +5599999999999):",
         bg="#f0f0f0",
         font=("Arial", 10),
         justify="center").pack(padx=10, pady=(10, 0), anchor="center")
numero_entry = tk.Entry(janela, width=30)
numero_entry.pack(padx=10, pady=(0,10))

tk.Button(janela,
          text="Compartilhar Link no WhatsApp",
          fg="white",
          bg="#128c7e",
          font=("Arial", 10, "bold"),
          relief="groove",
          bd=3,
          command=compartilhar).pack(pady=(0,10))

status_label = tk.Label(janela, text="", bg="#f0f0f0")
status_label.pack(pady=(0,10))

janela.mainloop()
