import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, scrolledtext
import winsound# For playing sounds
import threading

# 音を鳴らす関数
def play_error_sound():
    winsound.PlaySound("SystemHand", winsound.SND_ALIAS)


# メッセージをコンソール風に表示
def update_message(message, color="black"):
    message_console.config(state=tk.NORMAL)
    message_console.insert(tk.END, message + "\n", ("color", color))
    message_console.tag_config("color", foreground=color)
    message_console.config(state=tk.DISABLED)
    message_console.yview(tk.END)  # 自動スクロール

# 複数PDFファイルの暗号化
def ango(file_paths):
    up = user_pass_entry.get()
    urp = confirm_user_pass_entry.get()

    if not up or not urp:
        update_message("エラー: USER パスワードを入力してください", "red")
        sound_thread = threading.Thread(target=play_error_sound)
        sound_thread.start()
        return

    if up == urp:
        for file_path in file_paths:
            if not pdf_is_encrypted(file_path):
                doc = fitz.open(file_path)
                output_path = os.path.join(os.path.dirname(file_path), os.path.basename(file_path).replace(".pdf", "_encrypted.pdf"))
                doc.save(output_path, user_pw=up, encryption=fitz.PDF_ENCRYPT_AES_256, permissions=fitz.PDF_PERM_ACCESSIBILITY)
                update_message(f"{os.path.basename(file_path)} を暗号化しました", "green")
            else:
                update_message(f"エラー: {os.path.basename(file_path)} はすでに暗号化されています", "red")
                sound_thread = threading.Thread(target=play_error_sound)
                sound_thread.start()
    else:
        update_message("エラー: パスワードが一致していません", "red")
        sound_thread = threading.Thread(target=play_error_sound)
        sound_thread.start()

# 複数PDFファイルの復号
def hukugo(file_paths):
    pw = user_pass_entry.get()

    if not pw:
        update_message("エラー: USER パスワードを入力してください", "red")
        sound_thread = threading.Thread(target=play_error_sound)
        sound_thread.start()
        return

    for file_path in file_paths:
        if pdf_is_encrypted(file_path):
            pdf = fitz.open(file_path)
            if pdf.authenticate(pw):
                output_path = os.path.join(os.path.dirname(file_path), os.path.basename(file_path).replace(".pdf", "_decrypted.pdf"))
                pdf.save(output_path)
                update_message(f"{os.path.basename(file_path)} を復号しました", "green")
            else:
                update_message("承認エラー: 正しいパスワードを入力してください", "red")
                sound_thread = threading.Thread(target=play_error_sound)
                sound_thread.start()
        else:
            update_message(f"エラー: {os.path.basename(file_path)} は暗号化されていません", "red")
            sound_thread = threading.Thread(target=play_error_sound)
            sound_thread.start()

# PDFが暗号化されているか確認
def pdf_is_encrypted(file):
    pdf = fitz.Document(file)
    return pdf.is_encrypted

# ファイル選択ダイアログ（複数ファイル選択）
def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    return file_paths

# 暗号化ボタンがクリックされたとき
def encrypt_button_clicked():
    file_paths = select_files()
    if file_paths:
        ango(file_paths)

# 復号ボタンがクリックされたとき
def decrypt_button_clicked():
    file_paths = select_files()
    if file_paths:
        hukugo(file_paths)

# GUIのセットアップ
def setup_gui():
    global user_pass_entry, confirm_user_pass_entry, message_console

    root = tk.Tk()
    root.title("PDFファイルの暗号化・復号ツール")
    root.geometry("600x500")
    root.configure(bg="#e0f7fa")  # 青系の背景

    # タイトルラベル
    title_label = tk.Label(root, text="PDFファイルの暗号化・復号ツール", font=("MS Mincho", 18, "bold"), bg="#e0f7fa", fg="#0277bd")
    title_label.pack(pady=10)

    # 説明ラベル
    description_label = tk.Label(root, text="暗号化/復号したいPDFファイルを選択し、必要なパスワードを入力してください。", font=("MS Mincho", 12), bg="#e0f7fa")
    description_label.pack()

    # パスワード入力
    tk.Label(root, text="USER パスワード:", bg="#e0f7fa", font=("MS Mincho", 12)).pack()
    user_pass_entry = tk.Entry(root, show="*", width=30)
    user_pass_entry.pack()

    tk.Label(root, text="USER パスワード確認:", bg="#e0f7fa", font=("MS Mincho", 12)).pack()
    confirm_user_pass_entry = tk.Entry(root, show="*", width=30)
    confirm_user_pass_entry.pack()

    # 暗号化ボタン
    encrypt_button = tk.Button(root, text="暗号化", command=encrypt_button_clicked, width=20, bg="#0277bd", fg="white", font=("MS Mincho", 12, "bold"))
    encrypt_button.pack(pady=5)

    # 復号ボタン
    decrypt_button = tk.Button(root, text="復号", command=decrypt_button_clicked, width=20, bg="#0277bd", fg="white", font=("MS Mincho", 12, "bold"))
    decrypt_button.pack(pady=5)

    # メッセージ表示コンソール
    message_console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("MS Mincho", 12), state=tk.DISABLED, bg="#e0f4ff")
    message_console.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":

    setup_gui()
