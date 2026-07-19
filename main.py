import os
import customtkinter as ctk
from PIL import Image

from rsa_module import generate_keys
from aes_module import generate_aes_key

# =========================
# CREATE FOLDERS
# =========================

os.makedirs("encrypted", exist_ok=True)
os.makedirs("extracted", exist_ok=True)
os.makedirs("output", exist_ok=True)
os.makedirs("keys", exist_ok=True)

# =========================
# GENERATE KEYS
# =========================

if not os.path.exists("keys/public.pem"):
    generate_keys()

if not os.path.exists("keys/aes_key.bin"):
    generate_aes_key()

# =========================
# IMPORT UI
# =========================

from ui.sender_frame import SenderFrame
from ui.receiver_frame import ReceiverFrame

# =========================
# THEME — Light / Print-friendly
# =========================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SecureStego — Document Transfer System")
app.geometry("1100x800")
app.resizable(False, False)
app.configure(fg_color="#F0F2F5")   # abu-abu muda sebagai latar utama

try:
    app.iconbitmap("assets/icon.ico")
except:
    pass

# =========================
# HEADER FRAME
# =========================

header = ctk.CTkFrame(app, fg_color="#FFFFFF", corner_radius=0, height=100,
                       border_width=0)
header.pack(fill="x", padx=0, pady=0)
header.pack_propagate(False)

# Garis bawah header
divider_top = ctk.CTkFrame(app, height=3, fg_color="#2563A8", corner_radius=0)
divider_top.pack(fill="x")

# Left: Logo + Title
left_header = ctk.CTkFrame(header, fg_color="transparent")
left_header.pack(side="left", padx=30, pady=14)

try:
    logo_image = ctk.CTkImage(
        light_image=Image.open("assets/logo.png"),
        dark_image=Image.open("assets/logo.png"),
        size=(56, 56)
    )
    logo_label = ctk.CTkLabel(left_header, image=logo_image, text="")
    logo_label.pack(side="left", padx=(0, 14))
except:
    pass

title_col = ctk.CTkFrame(left_header, fg_color="transparent")
title_col.pack(side="left")

ctk.CTkLabel(
    title_col,
    text="SecureStego",
    font=("Arial", 26, "bold"),
    text_color="#1A3A6B"
).pack(anchor="w")

ctk.CTkLabel(
    title_col,
    text="Document Transfer System",
    font=("Arial", 12),
    text_color="#6B7A99"
).pack(anchor="w")

# Right: badge pills
right_header = ctk.CTkFrame(header, fg_color="transparent")
right_header.pack(side="right", padx=30, pady=14)

badges = [
    ("AES-256", "#1D4ED8", "#DBEAFE"),
    ("SHA-256", "#065F46", "#D1FAE5"),
    ("RSA",     "#6B21A8", "#EDE9FE"),
    ("Stegano", "#92400E", "#FEF3C7"),
]

for label, text_color, bg_color in badges:
    pill = ctk.CTkFrame(right_header, fg_color=bg_color, corner_radius=20,
                        height=28, border_width=1, border_color=text_color)
    pill.pack(side="left", padx=5, pady=5)
    ctk.CTkLabel(
        pill,
        text=f"  {label}  ",
        font=("Arial", 11, "bold"),
        text_color=text_color
    ).pack(padx=6, pady=2)

# =========================
# TAB VIEW
# =========================

tabview = ctk.CTkTabview(
    app,
    width=1060,
    height=630,
    fg_color="#FFFFFF",
    segmented_button_fg_color="#E2E8F0",
    segmented_button_selected_color="#2563A8",
    segmented_button_selected_hover_color="#1D4ED8",
    segmented_button_unselected_color="#E2E8F0",
    segmented_button_unselected_hover_color="#CBD5E1",
    text_color="#1A3A6B",
    border_color="#CBD5E1",
    border_width=1
)
tabview.pack(pady=10, padx=20)
tabview.add("  Sender  ")
tabview.add("  Receiver  ")

sender_tab   = tabview.tab("  Sender  ")
receiver_tab = tabview.tab("  Receiver  ")

SenderFrame(sender_tab)
ReceiverFrame(receiver_tab)

# =========================
# FOOTER
# =========================

footer = ctk.CTkFrame(app, fg_color="#FFFFFF", height=36, corner_radius=0,
                       border_width=0)
footer.pack(fill="x", padx=0, pady=(0, 0))
footer.pack_propagate(False)

ctk.CTkLabel(
    footer,
    text="© 2026 SecureStego  —  End-to-end encrypted document transfer",
    font=("Arial", 11),
    text_color="#64748B"
).pack(side="left", padx=24, pady=8)

ctk.CTkLabel(
    footer,
    text="● SECURE",
    font=("Arial", 11, "bold"),
    text_color="#065F46"
).pack(side="right", padx=24, pady=8)

app.mainloop()
