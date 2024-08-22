import tkinter as tk
from tkinter import filedialog, scrolledtext
import fitz  # PyMuPDF
import os
import threading
import winsound

class PDFTool:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback
        self.setup_pdf_tool()

    def setup_pdf_tool(self):
        # Clear the screen for transitions
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button
        back_button = tk.Button(self.root, text="ホームに戻る", command=self.go_back_callback)
        back_button.pack(pady=5)

        # Set up your PDF encryption/decryption GUI components
        label = tk.Label(self.root, text="PDF 暗号化/復号ツール", font=("MS Mincho", 18, "bold"))
        label.pack(pady=20)

        # Password input fields
        tk.Label(self.root, text="USER パスワード:").pack()
        self.user_pass_entry = tk.Entry(self.root, show="*", width=30)
        self.user_pass_entry.pack()

        tk.Label(self.root, text="USER パスワード確認:").pack()
        self.confirm_user_pass_entry = tk.Entry(self.root, show="*", width=30)
        self.confirm_user_pass_entry.pack()

        # Encrypt button
        encrypt_button = tk.Button(self.root, text="暗号化", command=self.encrypt_button_clicked)
        encrypt_button.pack(pady=5)

        # Decrypt button
        decrypt_button = tk.Button(self.root, text="復号", command=self.decrypt_button_clicked)
        decrypt_button.pack(pady=5)

        # Message console
        self.message_console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.message_console.pack(pady=10)

    def encrypt_button_clicked(self):
        file_paths = self.select_files()
        if file_paths:
            self.ango(file_paths)

    def decrypt_button_clicked(self):
        file_paths = self.select_files()
        if file_paths:
            self.hukugo(file_paths)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        return file_paths

    def ango(self, file_paths):
        up = self.user_pass_entry.get()
        urp = self.confirm_user_pass_entry.get()

        if not up or not urp:
            self.update_message("エラー: USER パスワードを入力してください", "red")
            threading.Thread(target=self.play_error_sound).start()
            return

        if up == urp:
            for file_path in file_paths:
                if not self.pdf_is_encrypted(file_path):
                    doc = fitz.open(file_path)
                    output_path = os.path.join(os.path.dirname(file_path), os.path.basename(file_path).replace(".pdf", "_encrypted.pdf"))
                    doc.save(output_path, user_pw=up, encryption=fitz.PDF_ENCRYPT_AES_256, permissions=fitz.PDF_PERM_ACCESSIBILITY)
                    self.update_message(f"{os.path.basename(file_path)} を暗号化しました", "green")
                else:
                    self.update_message(f"エラー: {os.path.basename(file_path)} はすでに暗号化されています", "red")
                    threading.Thread(target=self.play_error_sound).start()
        else:
            self.update_message("エラー: パスワードが一致していません", "red")
            threading.Thread(target=self.play_error_sound).start()

    def hukugo(self, file_paths):
        pw = self.user_pass_entry.get()

        if not pw:
            self.update_message("エラー: USER パスワードを入力してください", "red")
            threading.Thread(target=self.play_error_sound).start()
            return

        for file_path in file_paths:
            if self.pdf_is_encrypted(file_path):
                pdf = fitz.open(file_path)
                if pdf.authenticate(pw):
                    output_path = os.path.join(os.path.dirname(file_path), os.path.basename(file_path).replace(".pdf", "_decrypted.pdf"))
                    pdf.save(output_path)
                    self.update_message(f"{os.path.basename(file_path)} を復号しました", "green")
                else:
                    self.update_message("承認エラー: 正しいパスワードを入力してください", "red")
                    threading.Thread(target=self.play_error_sound).start()
            else:
                self.update_message(f"エラー: {os.path.basename(file_path)} は暗号化されていません", "red")
                threading.Thread(target=self.play_error_sound).start()

    def pdf_is_encrypted(self, file):
        pdf = fitz.Document(file)
        return pdf.is_encrypted

    def update_message(self, message, color="black"):
        self.message_console.config(state=tk.NORMAL)
        self.message_console.insert(tk.END, message + "\n", ("color", color))
        self.message_console.tag_config("color", foreground=color)
        self.message_console.config(state=tk.DISABLED)
        self.message_console.yview(tk.END)

    def play_error_sound(self):
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
