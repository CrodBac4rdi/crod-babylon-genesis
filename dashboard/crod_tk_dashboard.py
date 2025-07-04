#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import subprocess
import json
import threading
import time
from datetime import datetime

class CRODDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("CROD POLYGLOT CITY - Live Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='black')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', background='black', foreground='cyan', font=('Arial', 24, 'bold'))
        style.configure('District.TFrame', background='black', borderwidth=2, relief='ridge')
        style.configure('Status.TLabel', background='black', foreground='lime', font=('Consolas', 12))
        style.configure('Metric.TLabel', background='black', foreground='white', font=('Consolas', 10))
        
        self.districts = {}
        self.init_ui()
        
        # Start metrics thread
        self.running = True
        self.metrics_thread = threading.Thread(target=self.update_metrics_loop, daemon=True)
        self.metrics_thread.start()
    
    def init_ui(self):
        # Header
        header = ttk.Label(self.root, text="🏙️ CROD POLYGLOT CITY - LIVE METRICS", style='Title.TLabel')
        header.pack(pady=20)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Connecting to K8s...", style='Status.TLabel')
        self.status_label.pack()
        
        # Connection diagram
        self.canvas = tk.Canvas(self.root, width=1150, height=250, bg='black', highlightthickness=0)
        self.canvas.pack(pady=20)
        self.draw_connection_map()
        
        # Districts frame
        districts_frame = tk.Frame(self.root, bg='black')
        districts_frame.pack(fill='both', expand=True, padx=20)
        
        district_configs = [
            ("meta-chain", "Meta-Chain (Elixir)", "cyan"),
            ("pattern-district", "Pattern District (Rust)", "magenta"),
            ("memory-quarter", "Memory Quarter (Go)", "lime"),
            ("intelligence-hub", "Intelligence Hub (Python)", "orange")
        ]
        
        # Create 2x2 grid
        for i, (key, name, color) in enumerate(district_configs):
            frame = tk.Frame(districts_frame, bg='#111', highlightbackground=color, highlightthickness=2)
            frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Title
            title = tk.Label(frame, text=name, bg='#111', fg=color, font=('Arial', 14, 'bold'))
            title.pack(pady=10)
            
            # Status
            status = tk.Label(frame, text="Status: Unknown", bg='#111', fg='gray', font=('Consolas', 10))
            status.pack()
            
            # CPU
            cpu_frame = tk.Frame(frame, bg='#111')
            cpu_frame.pack(fill='x', padx=20, pady=5)
            cpu_label = tk.Label(cpu_frame, text="CPU: --", bg='#111', fg='white', font=('Consolas', 10))
            cpu_label.pack(side='left')
            cpu_bar = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
            cpu_bar.pack(side='right', padx=10)
            
            # Memory
            mem_frame = tk.Frame(frame, bg='#111')
            mem_frame.pack(fill='x', padx=20, pady=5)
            mem_label = tk.Label(mem_frame, text="Memory: --", bg='#111', fg='white', font=('Consolas', 10))
            mem_label.pack(side='left')
            mem_bar = ttk.Progressbar(mem_frame, length=200, mode='determinate')
            mem_bar.pack(side='right', padx=10)
            
            # Pod info
            pod_label = tk.Label(frame, text="Pod: --", bg='#111', fg='gray', font=('Consolas', 9))
            pod_label.pack(pady=5)
            
            self.districts[key] = {
                'frame': frame,
                'status': status,
                'cpu_label': cpu_label,
                'cpu_bar': cpu_bar,
                'mem_label': mem_label,
                'mem_bar': mem_bar,
                'pod_label': pod_label,
                'color': color
            }
            
            districts_frame.grid_columnconfigure(i%2, weight=1)
            districts_frame.grid_rowconfigure(i//2, weight=1)
    
    def draw_connection_map(self):
        # Gateway
        self.canvas.create_rectangle(500, 20, 650, 70, outline='yellow', width=2)
        self.canvas.create_text(575, 45, text="Gateway\n:30889", fill='yellow', font=('Arial', 12))
        
        # Redis (broken)
        self.canvas.create_rectangle(515, 100, 635, 140, outline='red', width=2, dash=(5, 5))
        self.canvas.create_text(575, 120, text="Redis\n(BROKEN)", fill='red', font=('Arial', 10))
        
        # Connection line
        self.canvas.create_line(575, 70, 575, 100, fill='yellow', width=2)
        
        # Districts
        positions = [(200, 180), (400, 180), (600, 180), (800, 180)]
        colors = ['cyan', 'magenta', 'lime', 'orange']
        names = ['Meta-Chain', 'Pattern', 'Memory', 'Intelligence']
        
        for (x, y), color, name in zip(positions, colors, names):
            self.canvas.create_rectangle(x-60, y-20, x+60, y+20, outline=color, width=2)
            self.canvas.create_text(x, y, text=name, fill=color, font=('Arial', 10))
            # Broken connection to Redis
            self.canvas.create_line(x, y-20, 575, 140, fill='red', width=1, dash=(3, 3))
    
    def get_k8s_data(self):
        try:
            # Get pods
            pod_result = subprocess.run(
                ['kubectl', 'get', 'pods', '-n', 'crod-polyglot', '-o', 'json'],
                capture_output=True, text=True, env={'KUBECONFIG': '/home/daniel/.kube/config'}
            )
            
            # Get metrics
            metrics_result = subprocess.run(
                ['kubectl', 'top', 'pods', '-n', 'crod-polyglot', '--no-headers'],
                capture_output=True, text=True, env={'KUBECONFIG': '/home/daniel/.kube/config'}
            )
            
            if pod_result.returncode == 0 and metrics_result.returncode == 0:
                pods_data = json.loads(pod_result.stdout)
                metrics_lines = metrics_result.stdout.strip().split('\n')
                
                metrics = {}
                for line in metrics_lines:
                    if line:
                        parts = line.split()
                        metrics[parts[0]] = {
                            'cpu': parts[1],
                            'memory': parts[2]
                        }
                
                return pods_data['items'], metrics
        except Exception as e:
            print(f"Error: {e}")
        
        return [], {}
    
    def update_metrics_loop(self):
        while self.running:
            pods, metrics = self.get_k8s_data()
            self.root.after(0, self.update_ui, pods, metrics)
            time.sleep(2)
    
    def update_ui(self, pods, metrics):
        self.status_label.config(text=f"Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Create pod lookup
        pod_lookup = {pod['metadata']['name']: pod for pod in pods}
        
        for key, widgets in self.districts.items():
            # Find matching pod
            found = False
            for pod_name, pod in pod_lookup.items():
                if key in pod_name:
                    found = True
                    
                    # Update status
                    ready = all(c['ready'] for c in pod['status'].get('containerStatuses', []))
                    if ready:
                        widgets['status'].config(text="Status: Running ✓", foreground=widgets['color'])
                    else:
                        widgets['status'].config(text=f"Status: {pod['status']['phase']}", foreground='red')
                    
                    # Update metrics
                    if pod_name in metrics:
                        m = metrics[pod_name]
                        cpu_value = int(m['cpu'].rstrip('m'))
                        mem_value = int(m['memory'].rstrip('Mi'))
                        
                        widgets['cpu_label'].config(text=f"CPU: {m['cpu']}")
                        widgets['cpu_bar']['value'] = min(100, cpu_value // 10)
                        
                        widgets['mem_label'].config(text=f"Memory: {m['memory']}")
                        widgets['mem_bar']['value'] = min(100, mem_value // 10)
                    
                    widgets['pod_label'].config(text=f"Pod: {pod_name}")
                    break
            
            if not found:
                widgets['status'].config(text="Status: Not Found", foreground='gray')
    
    def cleanup(self):
        self.running = False

def main():
    root = tk.Tk()
    dashboard = CRODDashboard(root)
    
    def on_closing():
        dashboard.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()