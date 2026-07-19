import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import base64

from aes_module import *
from hash_module import *
from rsa_module import *
from stegano_module import *

selected_document = ""
selected_image    = ""

aes_key = load_aes_key()
public_key, private_key = load_keys()

# ── helpers ───────────────────────────────────────────────────────────────────

def make_file_card(parent, icon, label_text):
    """Card pemilihan file — latar putih, border abu-abu."""
    card = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=10,
                        border_width=1, border_color="#CBD5E1")
    card.pack(fill="x", padx=0, pady=5)
    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="x", padx=14, pady=10)

    icon_box = ctk.CTkFrame(inner, fg_color="#E2E8F0", width=40, height=40,
                             corner_radius=20)
    icon_box.pack(side="left")
    icon_box.pack_propagate(False)
    ctk.CTkLabel(icon_box, text=icon, font=("Segoe UI Emoji", 16)).pack(expand=True)

    txt_col = ctk.CTkFrame(inner, fg_color="transparent")
    txt_col.pack(side="left", padx=12, fill="x", expand=True)
    ctk.CTkLabel(txt_col, text=label_text, font=("Arial", 11, "bold"),
                 text_color="#475569").pack(anchor="w")
    path_lbl = ctk.CTkLabel(txt_col, text="Tidak ada file dipilih",
                             font=("Arial", 10), text_color="#94A3B8")
    path_lbl.pack(anchor="w")
    return card, path_lbl


# ── SenderFrame ───────────────────────────────────────────────────────────────

class SenderFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF")
        self.pack(fill="both", expand=True)

        cols  = ctk.CTkFrame(self, fg_color="transparent")
        cols.pack(fill="both", expand=True, padx=16, pady=12)
        left  = ctk.CTkFrame(cols, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = ctk.CTkFrame(cols, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # ── LEFT ────────────────────────────────────────────────────────────
        ctk.CTkLabel(left, text="SENDER PANEL",
                     font=("Arial", 16, "bold"),
                     text_color="#1A3A6B").pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(left,
                     text="Enkripsi & sembunyikan dokumen ke dalam gambar",
                     font=("Arial", 11),
                     text_color="#64748B").pack(anchor="w", pady=(0, 14))

        # Card dokumen
        _doc_card, self.doc_label = make_file_card(left, "📄", "FILE DOKUMEN")
        ctk.CTkButton(
            left, text="  Pilih Dokumen",
            command=self.choose_document,
            font=("Arial", 12, "bold"), height=38, corner_radius=8,
            fg_color="#EFF6FF", hover_color="#DBEAFE",
            text_color="#1D4ED8", border_width=1, border_color="#93C5FD"
        ).pack(fill="x", pady=(0, 8))

        # Card cover image
        _img_card, self.img_label = make_file_card(left, "🖼️", "COVER IMAGE")
        ctk.CTkButton(
            left, text="  Pilih Gambar Cover",
            command=self.choose_image,
            font=("Arial", 12, "bold"), height=38, corner_radius=8,
            fg_color="#EFF6FF", hover_color="#DBEAFE",
            text_color="#1D4ED8", border_width=1, border_color="#93C5FD"
        ).pack(fill="x", pady=(0, 14))

        # Tombol aksi utama
        ctk.CTkButton(
            left, text="🔐  Encrypt & Hide",
            command=self.encrypt_and_hide,   # ← method milik class ini
            font=("Arial", 13, "bold"), height=44, corner_radius=10,
            fg_color="#2563A8", hover_color="#1D4ED8", text_color="#FFFFFF"
        ).pack(fill="x")

        self.status = ctk.CTkLabel(left, text="", font=("Arial", 11),
                                   text_color="#065F46")
        self.status.pack(pady=(8, 0))

        # Step indicator
        steps_frame = ctk.CTkFrame(left, fg_color="#F1F5F9", corner_radius=10,
                                   border_width=1, border_color="#E2E8F0")
        steps_frame.pack(fill="x", pady=(12, 0))
        steps_inner = ctk.CTkFrame(steps_frame, fg_color="transparent")
        steps_inner.pack(padx=14, pady=10)

        self.step_labels = []
        step_defs = [
            ("AES-256", "#1D4ED8"),
            ("SHA-256", "#065F46"),
            ("RSA Sign", "#6B21A8"),
            ("Stegano",  "#92400E"),
        ]
        for label, active_color in step_defs:
            col = ctk.CTkFrame(steps_inner, fg_color="transparent")
            col.pack(side="left", padx=12)
            dot = ctk.CTkFrame(col, fg_color="#CBD5E1", width=10, height=10,
                               corner_radius=5)
            dot.pack()
            lbl = ctk.CTkLabel(col, text=label, font=("Arial", 10),
                               text_color="#94A3B8")
            lbl.pack()
            self.step_labels.append((dot, lbl, active_color))

        # ── RIGHT: Log ──────────────────────────────────────────────────────
        ctk.CTkLabel(right, text="LOG OUTPUT",
                     font=("Arial", 11, "bold"),
                     text_color="#475569").pack(anchor="w", pady=(0, 6))
        self.log = ctk.CTkTextbox(
            right,
            font=("Courier New", 11),
            fg_color="#F8FAFC",
            text_color="#1E293B",
            border_color="#CBD5E1",
            border_width=1,
            corner_radius=10,
            wrap="word"
        )
        self.log.pack(fill="both", expand=True)
        self.log.insert("end", "SecureStego v1.0\n")
        self.log.insert("end", "─" * 38 + "\n")
        self.log.insert("end", "Menunggu aksi dari pengguna...\n")
        self.log.configure(state="disabled")

    # ── helpers (di dalam class) ──────────────────────────────────────────────

    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _activate_step(self, idx):
        dot, lbl, active_color = self.step_labels[idx]
        dot.configure(fg_color=active_color)
        lbl.configure(text_color=active_color)

    def _reset_steps(self):
        for dot, lbl, _ in self.step_labels:
            dot.configure(fg_color="#CBD5E1")
            lbl.configure(text_color="#94A3B8")

    # ── actions (di dalam class) ──────────────────────────────────────────────

    def choose_document(self):
        global selected_document
        path = filedialog.askopenfilename()
        if path:
            selected_document = path
            self.doc_label.configure(text=os.path.basename(path),
                                     text_color="#1E293B")

    def choose_image(self):
        global selected_image
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.bmp")])
        if path:
            selected_image = path
            self.img_label.configure(text=os.path.basename(path),
                                     text_color="#1E293B")

    def encrypt_and_hide(self):   # ← WAJIB di dalam class, indent 4 spasi
        global selected_document, selected_image

        if not selected_document or not selected_image:
            messagebox.showerror("Error",
                                 "Pilih dokumen dan gambar terlebih dahulu!")
            return

        self._reset_steps()
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self._log("[ START ] Memulai proses enkripsi...")
        self.status.configure(text="")

        try:
            # Step 1 — AES-256
            encrypt_file(selected_document, "encrypted/encrypted.bin", aes_key)
            self._activate_step(0)
            self._log("[  AES  ] Enkripsi AES-256 berhasil ✓")

            # Step 2 — SHA-256
            hash_value = generate_hash(selected_document)
            self._activate_step(1)
            self._log(f"[ HASH  ] SHA-256: {hash_value[:24]}...")

            # Step 3 — RSA sign
            sign_hash(hash_value, private_key)
            self._activate_step(2)
            self._log("[  RSA  ] Digital signature dibuat ✓")

            # Step 4 — Cek kapasitas gambar sebelum steganografi
            with open("encrypted/encrypted.bin", "rb") as f:
                data = f.read()

            original_filename = os.path.basename(selected_document)
            encoded           = base64.b64encode(data).decode()
            payload           = original_filename + "||" + encoded

            from PIL import Image as PILImage
            with PILImage.open(selected_image) as img:
                w, h = img.size
                kapasitas_byte = (w * h * 3) // 8

            payload_byte = len(payload.encode("utf-8"))

            if payload_byte > kapasitas_byte:
                kekurangan = payload_byte - kapasitas_byte
                min_px     = int((payload_byte * 8 / 3) ** 0.5) + 50
                self._log(f"[ ERROR ] Payload  : {payload_byte:,} byte")
                self._log(f"[ ERROR ] Kapasitas: {kapasitas_byte:,} byte")
                self._log(f"[ ERROR ] Kurang   : {kekurangan:,} byte")
                self._log(f"[ INFO  ] Gunakan gambar minimal {min_px}×{min_px} px")
                messagebox.showerror("Gambar Terlalu Kecil",
                    f"Cover image tidak cukup besar!\n\n"
                    f"Ukuran payload  : {payload_byte:,} byte\n"
                    f"Kapasitas gambar: {kapasitas_byte:,} byte\n\n"
                    f"Solusi: Gunakan gambar minimal {min_px}×{min_px} piksel.")
                return

            # Kapasitas cukup — lanjut steganografi
            hide_data(selected_image, payload, "output/secret_image.png")
            self._activate_step(3)
            self._log(f"[ STEGO ] Data + nama '{original_filename}' disembunyikan ✓")

            self._log("\n[ DONE  ] Output: output/secret_image.png")
            self._log("[ INFO  ] Nama file asli tersimpan di dalam gambar")
            self.status.configure(
                text="✓ Berhasil! secret_image.png tersimpan",
                text_color="#065F46")
            messagebox.showinfo("Berhasil",
                f"secret_image.png telah dibuat!\n\n"
                f"Nama file '{original_filename}' tersimpan di dalam gambar.\n"
                f"Receiver akan mendapat file dengan nama asli secara otomatis.")

        except Exception as e:
            self._log(f"[ ERROR ] {str(e)}")
            self.status.configure(text="✗ Terjadi kesalahan",
                                  text_color="#B91C1C")
            messagebox.showerror("Error", str(e))