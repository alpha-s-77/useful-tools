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

        # Title with modern font and style
        label = tk.Label(self.root, text="ツール選択画面", font=("Arial", 24, "bold"))
        label.pack(pady=30)

        # PDF Tool Button with modern styling
        pdf_button = tk.Button(self.root, text="PDF 暗号化/復号ツール", command=self.open_pdf_tool,
                               font=("Arial", 14), bg="#007BFF", fg="white", relief=tk.FLAT)
        pdf_button.pack(pady=10, fill=tk.X, padx=50)

        # JPG Tool Button with modern styling
        jpg_button = tk.Button(self.root, text="JPG 名前変更ツール", command=self.open_jpg_tool,
                               font=("Arial", 14), bg="#28a745", fg="white", relief=tk.FLAT)
        jpg_button.pack(pady=10, fill=tk.X, padx=50)

        # Exit Button with modern styling
        exit_button = tk.Button(self.root, text="終了", command=self.on_exit,
                                font=("Arial", 14), bg="#dc3545", fg="white", relief=tk.FLAT)
        exit_button.pack(pady=20)

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
