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

        # Back button
        back_button = tk.Button(self.root, text="ホームに戻る", command=self.go_back_callback)
        back_button.pack(pady=5)

        label = tk.Label(self.root, text="JPG 名前変更ツール", font=("MS Mincho", 18, "bold"))
        label.pack(pady=20)

        # Select folder button
        self.label = tk.Label(self.root, text="JPGファイルが含まれるフォルダーを選択してください:")
        self.label.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="参照", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        self.start_button = tk.Button(self.root, text="処理開始", command=self.start_processing)
        self.start_button.pack(pady=5)
        self.start_button.config(state=tk.DISABLED)

        self.folder_path = ""

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.start_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.DISABLED)

    def start_processing(self):
        if not self.folder_path:
            messagebox.showwarning("警告", "フォルダーを選択してください。")
            return

        pre_process_errors = self.pre_process_files()
        rename_errors = self.rename_files()

        self.show_results(pre_process_errors + rename_errors)

    def pre_process_files(self):
        c = 0
        errors = []

        for filename in tqdm(Path(self.folder_path).glob("*.JPG"), desc="事前処理中"):
            exif = self.get_exif_of_image(filename)
            if "DateTime" in exif:
                c += 1
            else:
                errors.append(f"{filename} に日付情報がありません")

        if c == 0:
            messagebox.showerror("エラー", "選択されたフォルダーには適切なJPGファイルがありません。")
        return errors

    def rename_files(self):
        c = 1
        errors = []

        for filename in tqdm(Path(self.folder_path).glob("*.JPG"), desc="ファイル名変更中"):
            try:
                # Get EXIF data and format the date string
                exif = self.get_exif_of_image(filename)
                date_str = exif["DateTime"].replace(":", "").replace(" ", "_")

                new_name = os.path.join(
                    os.path.dirname(filename),
                    f"{os.path.basename(self.folder_path)}_{c}_{date_str}.JPG"
                )

                os.rename(filename, new_name)
                c += 1

            except Exception as e:
                errors.append(f"{filename} の名前変更エラー: {str(e)}")

        return errors

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

