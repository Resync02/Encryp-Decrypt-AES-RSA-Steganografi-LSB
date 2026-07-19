import os
import subprocess
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
import base64

from aes_module    import *
from hash_module   import *
from rsa_module    import *
from stegano_module import *

aes_key = load_aes_key()
public_key, private_key = load_keys()
selected_secret = ""



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


def open_file(filepath):
    """Buka file dengan aplikasi default sesuai OS."""
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", filepath])
        else:
            subprocess.Popen(["xdg-open", filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Tidak bisa membuka file:\n{str(e)}")


# ── ReceiverFrame ─────────────────────────────────────────────────────────────

class ReceiverFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="#FFFFFF")
        self.pack(fill="both", expand=True)

        self.output_path = ""

        cols = ctk.CTkFrame(self, fg_color="transparent")
        cols.pack(fill="both", expand=True, padx=16, pady=12)

        left  = ctk.CTkFrame(cols, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        right = ctk.CTkFrame(cols, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # ── LEFT ────────────────────────────────────────────────────────────

        ctk.CTkLabel(left, text="RECEIVER PANEL",
                     font=("Arial", 16, "bold"),
                     text_color="#1A3A6B").pack(anchor="w", pady=(0, 2))
        ctk.CTkLabel(left,
                     text="Ekstrak & verifikasi dokumen dari gambar rahasia",
                     font=("Arial", 11), text_color="#64748B").pack(anchor="w", pady=(0, 14))

        # Card secret image
        _card, self.secret_label = make_file_card(left, "🔒", "SECRET IMAGE")

        ctk.CTkButton(
            left, text="  Pilih Secret Image",
            command=self.choose_secret,
            font=("Arial", 12, "bold"), height=38, corner_radius=8,
            fg_color="#F0FDF4", hover_color="#DCFCE7",
            text_color="#065F46", border_width=1, border_color="#86EFAC"
        ).pack(fill="x", pady=(0, 10))

        # Tombol aksi utama
        ctk.CTkButton(
            left, text="🔓  Extract & Verify",
            command=self.extract_verify,
            font=("Arial", 13, "bold"), height=44, corner_radius=10,
            fg_color="#065F46", hover_color="#047857", text_color="#FFFFFF"
        ).pack(fill="x")

        self.status = ctk.CTkLabel(left, text="", font=("Arial", 11))
        self.status.pack(pady=(8, 0))

        # ── Kotak hasil verifikasi ───────────────────────────────────────────
        self.result_box = ctk.CTkFrame(left, fg_color="#F8FAFC", corner_radius=12,
                                       border_width=1, border_color="#CBD5E1",
                                       height=105)
        self.result_box.pack(fill="x", pady=(12, 0))
        self.result_box.pack_propagate(False)

        self.result_icon = ctk.CTkLabel(self.result_box, text="—",
                                        font=("Segoe UI Emoji", 22))
        self.result_icon.pack(pady=(8, 0))

        self.result_text = ctk.CTkLabel(self.result_box,
                                        text="Menunggu verifikasi...",
                                        font=("Arial", 11, "bold"),
                                        text_color="#94A3B8")
        self.result_text.pack()

        self.result_filename = ctk.CTkLabel(self.result_box, text="",
                                            font=("Arial", 10),
                                            text_color="#64748B")
        self.result_filename.pack()

        # Tombol buka file — tersembunyi awalnya
        self.open_btn = ctk.CTkButton(
            left, text="📂  Buka File Hasil",
            command=self.open_result,
            font=("Arial", 12, "bold"), height=38, corner_radius=8,
            fg_color="#EFF6FF", hover_color="#DBEAFE",
            text_color="#1D4ED8", border_width=1, border_color="#93C5FD"
        )

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

    # ── helpers ──────────────────────────────────────────────────────────────

    def _log(self, msg):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ── actions ──────────────────────────────────────────────────────────────

    def choose_secret(self):
        global selected_secret
        path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if path:
            selected_secret = path
            self.secret_label.configure(text=os.path.basename(path),
                                        text_color="#1E293B")

    def open_result(self):
        if self.output_path and os.path.exists(self.output_path):
            open_file(self.output_path)
        else:
            messagebox.showwarning("File tidak ditemukan",
                                   "File hasil tidak ditemukan.")

    def extract_verify(self):
        global selected_secret
        if not selected_secret:
            messagebox.showerror("Error", "Pilih secret image terlebih dahulu!")
            return

        # Reset UI
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self.open_btn.pack_forget()
        self.result_box.configure(border_color="#CBD5E1", fg_color="#F8FAFC")
        self.result_icon.configure(text="⏳")
        self.result_text.configure(text="Memproses...", text_color="#92400E")
        self.result_filename.configure(text="")
        self.status.configure(text="")
        self._log("[ START ] Memulai ekstraksi...")

        try:
            # Step 1 — Ekstrak LSB
            hidden_data = reveal_data(selected_secret)
            self._log("[ STEGO ] Data berhasil diekstrak dari gambar ✓")

            # Step 2 — Pisahkan metadata nama file
            if "||" in hidden_data:
                original_filename, encoded = hidden_data.split("||", 1)
                self._log(f"[ INFO  ] Nama file asli: '{original_filename}'")
            else:
                original_filename = "decrypted_file"
                encoded = hidden_data
                self._log("[ WARN  ] Metadata tidak ditemukan, nama default digunakan")

            # Step 3 — Decode Base64 & simpan ciphertext
            encrypted_binary = base64.b64decode(encoded.encode())
            with open("extracted/extracted.bin", "wb") as f:
                f.write(encrypted_binary)
            self._log("[  AES  ] Decryption AES-256 dimulai...")

            # Step 4 — Dekripsi dengan nama file asli
            output_path = os.path.join("extracted", original_filename)
            decrypt_file("extracted/extracted.bin", output_path, aes_key)
            self.output_path = output_path
            self._log("[  AES  ] Decryption berhasil ✓")
            self._log(f"[ FILE  ] Disimpan: extracted/{original_filename}")

            # Step 5 — Hash hasil dekripsi
            hash_value = generate_hash(output_path)
            self._log(f"[ HASH  ] SHA-256: {hash_value[:24]}...")

            # Step 6 — Verifikasi RSA
            valid = verify_signature(hash_value, public_key)

            if valid:
                self._log("\n[  RSA  ] ✓ SIGNATURE VALID — File aman")
                self._log(f"\n[ DONE  ] File siap dibuka: extracted/{original_filename}")

                # UI: status VALID (hijau)
                self.result_box.configure(border_color="#16A34A", fg_color="#F0FDF4")
                self.result_icon.configure(text="✅")
                self.result_text.configure(text="SIGNATURE VALID  —  FILE AMAN",
                                           text_color="#065F46")
                self.result_filename.configure(
                    text=f"📄 extracted/{original_filename}",
                    text_color="#1D4ED8")
                self.status.configure(text="✓ Verifikasi berhasil",
                                      text_color="#065F46")
                self.open_btn.pack(fill="x", pady=(10, 0))
                messagebox.showinfo("Berhasil ✓",
                    f"VALID SIGNATURE — File aman!\n\n"
                    f"File tersimpan di:\nextracted/{original_filename}\n\n"
                    f"Klik 'Buka File Hasil' untuk membukanya langsung.")
            else:
                self._log("\n[  RSA  ] ✗ SIGNATURE INVALID — File dimodifikasi!")
                self._log(f"\n[ DONE  ] File disimpan (dengan peringatan): extracted/{original_filename}")

                # UI: status INVALID (merah)
                self.result_box.configure(border_color="#DC2626", fg_color="#FFF1F2")
                self.result_icon.configure(text="❌")
                self.result_text.configure(text="SIGNATURE INVALID  —  DIMODIFIKASI",
                                           text_color="#B91C1C")
                self.result_filename.configure(
                    text=f"⚠️ extracted/{original_filename}",
                    text_color="#B45309")
                self.result_box.configure(border_color="#DC2626")
                self.status.configure(text="✗ Verifikasi gagal",
                                      text_color="#B91C1C")
                self.open_btn.pack(fill="x", pady=(10, 0))
                messagebox.showwarning("Peringatan ✗",
                    f"INVALID SIGNATURE!\nFile mungkin telah dimodifikasi.\n\n"
                    f"File tetap disimpan di:\nextracted/{original_filename}\n\n"
                    f"Gunakan dengan hati-hati.")

        except Exception as e:
            self._log(f"[ ERROR ] {str(e)}")
            self.result_box.configure(border_color="#DC2626", fg_color="#FFF1F2")
            self.result_icon.configure(text="⚠️")
            self.result_text.configure(text="TERJADI KESALAHAN",
                                       text_color="#B91C1C")
            self.status.configure(text="✗ Error", text_color="#B91C1C")
            messagebox.showerror("Error", str(e))
