import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os
import datetime
from PIL import Image, ExifTags
from tqdm import tqdm

class JPGTool:
    def __init__(self, root, go_back_callback):
        self.root = root
        self.go_back_callback = go_back_callback
        self.setup_jpg_tool()

    def setup_jpg_tool(self):
                # Clear the screen for transitions
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button with modern styling
        back_button = tk.Button(self.root, text="ホームに戻る", command=self.go_back_callback,
                                font=("Arial", 12), bg="#007BFF", fg="white", relief=tk.FLAT)
        back_button.pack(pady=10)

        # Title with modern font and style
        label = tk.Label(self.root, text="JPG 名前変更ツール", font=("Arial", 24, "bold"))
        label.pack(pady=30)

        # Folder selection label and button
        self.label = tk.Label(self.root, text="JPGファイルが含まれるフォルダーを選択してください:", font=("Arial", 12))
        self.label.pack(pady=20)

        self.browse_button = tk.Button(self.root, text="　参照　", command=self.browse_folder,
                                       font=("Arial", 12), bg="#28a745", fg="white", relief=tk.FLAT)
        self.browse_button.pack(pady=10)

        self.start_button = tk.Button(self.root, text="処理開始", command=self.start_processing,
                                      font=("Arial", 12), bg="#ffc107", fg="black", relief=tk.FLAT)
        self.start_button.pack(pady=10)
        self.start_button.config(state=tk.DISABLED)

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def pre_process_files(self):
        c = 0
        errors = []

        # Match files with any case variation of ".jpg"
        for filename in tqdm(Path(self.folder_path).glob("*.jp*g"), desc="事前処理中"):
            exif = self.get_exif_of_image(filename)
            if "DateTimeOriginal" in exif:
                try:
                    new_name = Path(filename).with_name(
                        datetime.datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S").strftime("%m%d-%H%M%S")
                    )
                    new_name_with_id = Path(self.folder_path) / f"{new_name}-{c}.jpg"  # Always use .jpg as output
                    os.rename(filename, new_name_with_id)
                    c += 1
                except Exception as e:
                    errors.append(f"[エラー] {filename}: {str(e)}")
            else:
                pass

        return errors

    def rename_files(self):
        c = 0
        errors = []

        # Match files with any case variation of ".jpg"
        for filename in tqdm(Path(self.folder_path).glob("*.jp*g"), desc="ファイル名変更中"):
            exif = self.get_exif_of_image(filename)
            if "DateTimeOriginal" in exif:
                try:
                    new_name = Path(filename).with_name(
                        datetime.datetime.strptime(exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S").strftime("%m%d-%H%M%S.jpg")
                    )
                    new_name_with_id = Path(self.folder_path) / f"[{c}] {new_name.name}"
                    os.rename(filename, new_name_with_id)
                    c += 1
                except Exception as e:
                    errors.append(f"[エラー] {filename}: {str(e)}")
            else:
                errors.append(f"[警告] {filename}: EXIFデータが見つかりません")

        return errors

    def start_processing(self):
        if not self.folder_path:
            messagebox.showwarning("警告", "フォルダーを選択してください。")
            return

        pre_process_errors = self.pre_process_files()
        rename_errors = self.rename_files()

        self.show_results(pre_process_errors + rename_errors)

    def get_exif_of_image(self, filepath):
        try:
            img = Image.open(filepath)
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in ExifTags.TAGS
            }
            return exif
        except Exception as e:
            messagebox.showerror("エラー", f"{filepath} のEXIFデータを取得できませんでした。: {str(e)}")
            return {}

    def show_results(self, errors):
        if errors:
            error_msg = "\n".join(errors)
            messagebox.showwarning("処理結果", f"エラーが発生しました:\n{error_msg}")
        else:
            messagebox.showinfo("処理結果", "全てのファイルの名前変更が完了しました。")

