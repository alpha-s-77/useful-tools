import tkinter as tk
from pdf_tool import PDFTool
from jpg_tool import JPGTool

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ツール選択画面")
        self.root.geometry("400x300")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)  # Handle the close button

        self.show_home_screen()

    def show_home_screen(self):
        # Clear the screen for transitions
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="ツール選択画面", font=("MS Mincho", 18, "bold"))
        label.pack(pady=20)

        # PDF Tool Button
        pdf_button = tk.Button(self.root, text="PDF 暗号化/復号ツール", command=self.open_pdf_tool)
        pdf_button.pack(pady=10)

        # JPG Tool Button
        jpg_button = tk.Button(self.root, text="JPG 名前変更ツール", command=self.open_jpg_tool)
        jpg_button.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(self.root, text="終了", command=self.on_exit)
        exit_button.pack(pady=10)

    def open_pdf_tool(self):
        # Open PDF Tool without closing the window
        PDFTool(self.root, self.show_home_screen)

    def open_jpg_tool(self):
        # Open JPG Tool without closing the window
        JPGTool(self.root, self.show_home_screen)

    def on_exit(self):
        self.root.quit()  # Safely exit the application

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
