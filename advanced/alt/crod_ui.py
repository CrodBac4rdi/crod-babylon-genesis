import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess

class CRODGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CROD Mental Systems")
        self.root.geometry("800x600")
        
        # Title
        title = tk.Label(self.root, text="CROD MENTAL SYSTEMS", font=("Arial", 20))
        title.pack(pady=10)
        
        # Input
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=10)
        
        self.input_text = ttk.Entry(self.input_frame, width=50)
        self.input_text.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.input_frame, text="Process", command=self.process).pack(side=tk.LEFT)
        
        # Output
        self.output = scrolledtext.ScrolledText(self.root, height=20, width=80)
        self.output.pack(pady=10)
        
        # Status
        self.status = tk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status.pack(fill=tk.X, side=tk.BOTTOM)
        
    def process(self):
        text = self.input_text.get()
        # Hier würde CROD processing hin
        self.output.insert(tk.END, f"Processing: {text}\n")
        self.input_text.delete(0, tk.END)
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = CRODGui()
    app.run()