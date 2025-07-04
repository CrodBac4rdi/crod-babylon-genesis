# crod_fantasy_ui.py - All-in-One Fantasy UI
# EINFACH STARTEN: python crod_fantasy_ui.py

import tkinter as tk
from tkinter import ttk, font
import json
import random
import math
from datetime import datetime
from crod_engine import CRODEngine

class CRODFantasyUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CROD Mental Systems - Fantasy UI")
        self.root.geometry("1400x900")
        
        # Dark Fantasy Colors
        self.colors = {
            'bg': '#0a0a0f',
            'panel': '#1a1a2e',
            'gold': '#FFD700',
            'purple': '#9370DB',
            'cyan': '#00CED1',
            'green': '#32CD32',
            'red': '#FF6347',
            'text': '#e8d5b7'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Initialize Engine
        self.engine = CRODEngine()
        
        # Player Stats
        self.player_stats = {
            'level': 1,
            'exp': 0,
            'exp_to_next': 100,
            'title': 'Novice Pattern Seeker',
            'str': 10,
            'agi': 10,
            'int': 10,
            'patterns_found': 0,
            'messages': 0
        }
        
        # Initialize UI
        self.setup_ui()
        self.create_particles()
        self.update_stats_display()
        
    def setup_ui(self):
        # Custom Fonts
        title_font = font.Font(family='Georgia', size=28, weight='bold')
        header_font = font.Font(family='Georgia', size=16, weight='bold')
        
        # Main Container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main_frame, 
                        text="✦ CROD MENTAL SYSTEMS ✦",
                        font=title_font,
                        fg=self.colors['gold'],
                        bg=self.colors['bg'])
        title.pack(pady=(0, 20))
        
        # Create 3 columns
        columns = tk.Frame(main_frame, bg=self.colors['bg'])
        columns.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel - Status Window
        self.create_status_panel(columns)
        
        # Center Panel - Main Interface
        self.create_main_panel(columns)
        
        # Right Panel - Visualization
        self.create_viz_panel(columns)
        
    def create_status_panel(self, parent):
        # Status Frame
        status_frame = self.create_magical_frame(parent, "STATUS WINDOW", side=tk.LEFT, fill=tk.BOTH)
        
        # Level Display
        level_frame = tk.Frame(status_frame, bg=self.colors['panel'])
        level_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.title_label = tk.Label(level_frame,
                                   text=self.player_stats['title'],
                                   font=('Arial', 12, 'italic'),
                                   fg=self.colors['cyan'],
                                   bg=self.colors['panel'])
        self.title_label.pack()
        
        self.level_label = tk.Label(level_frame,
                                   text=f"Level {self.player_stats['level']}",
                                   font=('Arial', 20, 'bold'),
                                   fg=self.colors['gold'],
                                   bg=self.colors['panel'])
        self.level_label.pack()
        
        # EXP Bar
        exp_frame = tk.Frame(status_frame, bg=self.colors['panel'])
        exp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.exp_canvas = tk.Canvas(exp_frame, height=20, bg='#333', highlightthickness=0)
        self.exp_canvas.pack(fill=tk.X)
        self.update_exp_bar()
        
        self.exp_label = tk.Label(exp_frame,
                                 text=f"{self.player_stats['exp']}/{self.player_stats['exp_to_next']} EXP",
                                 font=('Arial', 10),
                                 fg=self.colors['text'],
                                 bg=self.colors['panel'])
        self.exp_label.pack()
        
        # Stats
        stats_frame = tk.Frame(status_frame, bg=self.colors['panel'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # STR/AGI/INT in a row
        stat_row = tk.Frame(stats_frame, bg=self.colors['panel'])
        stat_row.pack()
        
        self.str_label = self.create_stat_display(stat_row, "STR", self.player_stats['str'], self.colors['red'])
        self.agi_label = self.create_stat_display(stat_row, "AGI", self.player_stats['agi'], self.colors['green'])
        self.int_label = self.create_stat_display(stat_row, "INT", self.player_stats['int'], self.colors['cyan'])
        
        # Quest Log
        quest_frame = self.create_magical_frame(status_frame, "ACTIVE QUESTS", fill=tk.X)
        
        quest_text = "▸ Process 10 Messages\n"
        quest_text += f"  Progress: {min(self.player_stats['messages'], 10)}/10\n\n"
        quest_text += "▸ Find 5 Patterns\n"
        quest_text += f"  Progress: {min(self.player_stats['patterns_found'], 5)}/5"
        
        quest_label = tk.Label(quest_frame,
                              text=quest_text,
                              font=('Arial', 10),
                              fg=self.colors['text'],
                              bg=self.colors['panel'],
                              justify=tk.LEFT)
        quest_label.pack(padx=10, pady=5)
        
    def create_main_panel(self, parent):
        # Main Frame
        main_frame = self.create_magical_frame(parent, "COMMAND INTERFACE", side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Chat Display
        self.chat_frame = tk.Frame(main_frame, bg='black')
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(self.chat_frame,
                                   bg='black',
                                   fg=self.colors['text'],
                                   font=('Consolas', 10),
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure tags
        self.chat_display.tag_config('system', foreground=self.colors['green'])
        self.chat_display.tag_config('user', foreground=self.colors['gold'])
        self.chat_display.tag_config('pattern', foreground=self.colors['purple'])
        self.chat_display.tag_config('error', foreground=self.colors['red'])
        self.chat_display.tag_config('levelup', foreground=self.colors['gold'], font=('Arial', 12, 'bold'))
        
        # Initial messages
        self.add_chat_message("System", "CROD Mental Systems initialized...", 'system')
        self.add_chat_message("System", "Ready for commands.", 'system')
        
        # Input Frame
        input_frame = tk.Frame(main_frame, bg=self.colors['panel'])
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.input_entry = tk.Entry(input_frame,
                                   bg='#222',
                                   fg='white',
                                   insertbackground='white',
                                   font=('Arial', 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self.process_input)
        
        send_btn = self.create_fantasy_button(input_frame, "EXECUTE", self.process_input)
        send_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Quick Commands
        quick_frame = tk.Frame(main_frame, bg=self.colors['panel'])
        quick_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        quick_commands = [
            ("Test Pattern", "ich halt bruh"),
            ("Show Stats", "stats"),
            ("Save State", "save")
        ]
        
        for text, cmd in quick_commands:
            btn = tk.Button(quick_frame,
                           text=text,
                           command=lambda c=cmd: self.quick_command(c),
                           bg=self.colors['purple'],
                           fg='white',
                           font=('Arial', 9),
                           relief=tk.FLAT,
                           padx=10)
            btn.pack(side=tk.LEFT, padx=2)
            
    def create_viz_panel(self, parent):
        # Visualization Frame
        viz_frame = self.create_magical_frame(parent, "PATTERN VISUALIZATION", side=tk.LEFT, fill=tk.BOTH)
        
        # Canvas for visualization
        self.viz_canvas = tk.Canvas(viz_frame,
                                   bg='#0a0a0f',
                                   highlightthickness=1,
                                   highlightbackground=self.colors['gold'])
        self.viz_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pattern nodes
        self.nodes = {}
        self.create_pattern_viz()
        
        # Stats display
        stats_frame = tk.Frame(viz_frame, bg=self.colors['panel'])
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.stats_label = tk.Label(stats_frame,
                                   text="Patterns: 0 | Atoms: 0 | Connections: 0",
                                   font=('Arial', 10),
                                   fg=self.colors['text'],
                                   bg=self.colors['panel'])
        self.stats_label.pack()
        
    def create_magical_frame(self, parent, title, **pack_options):
        # Container
        container = tk.Frame(parent, bg=self.colors['bg'])
        container.pack(padx=5, pady=5, **pack_options)
        
        # Title
        title_label = tk.Label(container,
                              text=title,
                              font=('Arial', 12, 'bold'),
                              fg=self.colors['gold'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        # Frame with border effect
        frame = tk.Frame(container,
                        bg=self.colors['panel'],
                        highlightbackground=self.colors['gold'],
                        highlightthickness=2)
        frame.pack(fill=tk.BOTH, expand=True)
        
        return frame
        
    def create_stat_display(self, parent, name, value, color):
        frame = tk.Frame(parent, bg=self.colors['panel'])
        frame.pack(side=tk.LEFT, padx=20)
        
        name_label = tk.Label(frame,
                             text=name,
                             font=('Arial', 10),
                             fg=color,
                             bg=self.colors['panel'])
        name_label.pack()
        
        value_label = tk.Label(frame,
                              text=str(value),
                              font=('Arial', 16, 'bold'),
                              fg='white',
                              bg=self.colors['panel'])
        value_label.pack()
        
        return value_label
        
    def create_fantasy_button(self, parent, text, command):
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=self.colors['gold'],
                       fg='black',
                       font=('Arial', 10, 'bold'),
                       relief=tk.FLAT,
                       padx=20,
                       pady=5)
        return btn
        
    def add_chat_message(self, sender, message, tag=''):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'system')
        self.chat_display.insert(tk.END, f"{sender}: ", tag if tag else 'user')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        
    def process_input(self, event=None):
        text = self.input_entry.get().strip()
        if not text:
            return
            
        self.input_entry.delete(0, tk.END)
        self.add_chat_message("You", text, 'user')
        
        # Process with engine
        if text.lower() == 'stats':
            self.show_stats()
        elif text.lower() == 'save':
            self.save_state()
        else:
            result = self.engine.process(text)
            
            if result.get('patterns'):
                patterns_str = ', '.join(result['patterns'])
                self.add_chat_message("System", f"Patterns detected: {patterns_str}", 'pattern')
                self.player_stats['patterns_found'] += len(result['patterns'])
                
            self.player_stats['messages'] += 1
            self.player_stats['exp'] += 10
            
            # Check level up
            if self.player_stats['exp'] >= self.player_stats['exp_to_next']:
                self.level_up()
                
            self.update_stats_display()
            self.update_pattern_viz()
            
    def quick_command(self, command):
        self.input_entry.insert(0, command)
        self.process_input()
        
    def level_up(self):
        self.player_stats['level'] += 1
        self.player_stats['exp'] = 0
        self.player_stats['exp_to_next'] = 100 * self.player_stats['level']
        self.player_stats['str'] += random.randint(1, 3)
        self.player_stats['agi'] += random.randint(1, 3)
        self.player_stats['int'] += random.randint(1, 3)
        
        # Update title
        if self.player_stats['level'] >= 10:
            self.player_stats['title'] = "CROD Master"
        elif self.player_stats['level'] >= 5:
            self.player_stats['title'] = "Pattern Hunter"
        else:
            self.player_stats['title'] = "Apprentice Debugger"
            
        self.add_chat_message("System", f"🎉 LEVEL UP! You are now level {self.player_stats['level']}!", 'levelup')
        
    def update_stats_display(self):
        self.level_label.config(text=f"Level {self.player_stats['level']}")
        self.title_label.config(text=self.player_stats['title'])
        self.exp_label.config(text=f"{self.player_stats['exp']}/{self.player_stats['exp_to_next']} EXP")
        self.str_label.config(text=str(self.player_stats['str']))
        self.agi_label.config(text=str(self.player_stats['agi']))
        self.int_label.config(text=str(self.player_stats['int']))
        
        self.update_exp_bar()
        
    def update_exp_bar(self):
        self.exp_canvas.delete('all')
        width = self.exp_canvas.winfo_width()
        if width > 1:
            exp_width = (self.player_stats['exp'] / self.player_stats['exp_to_next']) * width
            self.exp_canvas.create_rectangle(0, 0, exp_width, 20,
                                           fill=self.colors['green'],
                                           outline='')
                                           
    def create_pattern_viz(self):
        # Create some nodes
        self.viz_canvas.delete('all')
        width = 300
        height = 300
        center_x = width // 2
        center_y = height // 2
        
        # Draw magic circle
        self.viz_canvas.create_oval(center_x - 100, center_y - 100,
                                   center_x + 100, center_y + 100,
                                   outline=self.colors['gold'],
                                   width=2)
                                   
        # Draw inner circle
        self.viz_canvas.create_oval(center_x - 70, center_y - 70,
                                   center_x + 70, center_y + 70,
                                   outline=self.colors['purple'],
                                   width=1)
                                   
    def update_pattern_viz(self):
        # Add random particle effect
        width = self.viz_canvas.winfo_width()
        height = self.viz_canvas.winfo_height()
        
        if width > 1:
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            
            particle = self.viz_canvas.create_oval(x-2, y-2, x+2, y+2,
                                                 fill=self.colors['cyan'],
                                                 outline='')
            self.animate_particle_fade(particle)
            
    def animate_particle_fade(self, particle):
        def fade():
            self.viz_canvas.delete(particle)
        self.root.after(1000, fade)
        
    def create_particles(self):
        # Background particles effect
        pass  # Simplified for performance
        
    def show_stats(self):
        stats = self.engine.get_stats()
        message = f"Engine Stats - Version: {stats['version']}, "
        message += f"Processed: {stats['processed']}, "
        message += f"Patterns Hit: {len(stats.get('pattern_hits', {}))}"
        self.add_chat_message("System", message, 'system')
        
    def save_state(self):
        self.engine.save_state()
        self.add_chat_message("System", "State saved successfully!", 'system')
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = CRODFantasyUI()
    app.run()