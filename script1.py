import customtkinter as ctk
import pyqrcode
from PIL import Image, ImageTk
import webbrowser
import re
import os

def limpar_campos():
    link_entry.delete(0, "end")
    numero_entry.delete(0, "end")
    img_label.configure(image=img_tk_placeholder, text="")
    status_label.configure(text="", text_color="black")

def gerar_qr():
    link = link_entry.get().strip()
    if not link:
        status_label.configure(text="⚠️ Por favor, insira uma URL.", text_color="orange")
        return
    if not re.match(r'^https?://[^\s]+$', link):
        status_label.configure(text="❌ URL inválida. Use http:// ou https://", text_color="red")
        return
    try:
        qr = pyqrcode.create(link)
        qr.png("temp_qr.png", scale=10)
        img = Image.open("temp_qr.png").convert("RGB").resize((260, 260))
        img.save("QRCode.png")
        global img_tk
        img_tk = ImageTk.PhotoImage(img)
        img_label.configure(image=img_tk, text="")
        status_label.configure(text="✅ QR Code gerado com sucesso!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Erro ao gerar: {str(e)}", text_color="red")

def compartilhar():
    numero = numero_entry.get().strip()
    link = link_entry.get().strip()
    if not re.match(r'^\+\d{10,15}$', numero):
        status_label.configure(text="❌ Número inválido. Use o formato +55XXXXXXXXXXX", text_color="red")
        return
    if not link or not re.match(r'^https?://[^\s]+$', link):
        status_label.configure(text="⚠️ Gere um QR Code com uma URL válida antes de compartilhar.", text_color="orange")
        return
    whatsapp_link = f"https://wa.me/{numero[1:]}?text={link}"
    webbrowser.open(whatsapp_link)
    status_label.configure(text="📲 Abrindo WhatsApp Web...", text_color="blue")
    numero_entry.delete(0, "end")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("QR & WhatsApp Generator")
app.geometry("420x640")
app.resizable(False, False)

ctk.CTkLabel(app, text="🔧 Gerador de QR Code & WhatsApp", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))

ctk.CTkLabel(app, text="Insira a URL:", anchor="w").pack(pady=(5, 0), padx=20, fill="x")
link_entry = ctk.CTkEntry(app, width=360, placeholder_text="https://exemplo.com")
link_entry.pack(pady=5)

ctk.CTkButton(app, text="🧾 Gerar QR Code", command=gerar_qr).pack(pady=(5, 15))

img_placeholder = Image.new("RGB", (260, 260), "#d9d9d9")
img_tk_placeholder = ImageTk.PhotoImage(img_placeholder)
img_label = ctk.CTkLabel(app, image=img_tk_placeholder, text="")
img_label.pack(pady=10)

ctk.CTkLabel(app, text="Número WhatsApp (ex: +5599999999999):", anchor="w").pack(pady=(5, 0), padx=20, fill="x")
numero_entry = ctk.CTkEntry(app, width=240, placeholder_text="+55...")
numero_entry.pack(pady=5)

ctk.CTkButton(app, text="📤 Compartilhar no WhatsApp", command=compartilhar, fg_color="#128c7e", hover_color="#0e6e5f").pack(pady=(10, 5))
ctk.CTkButton(app, text="🧹 Limpar Tudo", command=limpar_campos, fg_color="#999").pack(pady=5)

status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12))
status_label.pack(pady=(10, 10))

app.mainloop()
