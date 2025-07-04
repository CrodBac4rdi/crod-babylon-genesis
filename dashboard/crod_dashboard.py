#!/usr/bin/env python3

import sys
import json
import subprocess
import time
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import pyqtgraph as pg

class MetricsWorker(QThread):
    metrics_updated = pyqtSignal(dict)
    
    def run(self):
        while True:
            try:
                # Get pod info
                pod_result = subprocess.run(
                    ['/usr/local/bin/kubectl', 'get', 'pods', '-n', 'crod-polyglot', '-o', 'json'],
                    capture_output=True, text=True, env={'KUBECONFIG': '/home/daniel/.kube/config'}
                )
                
                # Get metrics
                metrics_result = subprocess.run(
                    ['/usr/local/bin/kubectl', 'top', 'pods', '-n', 'crod-polyglot', '--no-headers'],
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
                                'cpu': int(parts[1].rstrip('m')),
                                'memory': int(parts[2].rstrip('Mi'))
                            }
                    
                    # Combine data
                    combined = {
                        'pods': pods_data['items'],
                        'metrics': metrics,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    self.metrics_updated.emit(combined)
                
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(2)

class DistrictWidget(QWidget):
    def __init__(self, name, color):
        super().__init__()
        self.name = name
        self.color = color
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        self.title = QLabel(self.name)
        self.title.setStyleSheet(f"""
            QLabel {{
                color: {self.color};
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid {self.color};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(self.title)
        
        # Status
        self.status_label = QLabel("Status: Unknown")
        self.status_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # CPU Progress
        self.cpu_label = QLabel("CPU: --")
        layout.addWidget(self.cpu_label)
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {self.color};
                border-radius: 3px;
                text-align: center;
                background: #111;
            }}
            QProgressBar::chunk {{
                background: {self.color};
            }}
        """)
        layout.addWidget(self.cpu_progress)
        
        # Memory Progress
        self.memory_label = QLabel("Memory: --")
        layout.addWidget(self.memory_label)
        self.memory_progress = QProgressBar()
        self.memory_progress.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {self.color};
                border-radius: 3px;
                text-align: center;
                background: #111;
            }}
            QProgressBar::chunk {{
                background: {self.color};
            }}
        """)
        layout.addWidget(self.memory_progress)
        
        # Pod info
        self.pod_info = QLabel("Pod: --")
        self.pod_info.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.pod_info)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background: rgba(0, 0, 0, 0.9);
                border: 1px solid #333;
                border-radius: 10px;
                padding: 10px;
            }
        """)
    
    def update_metrics(self, pod_data, metrics):
        if pod_data:
            # Status
            status = pod_data['status']['phase']
            ready = all(c['ready'] for c in pod_data['status'].get('containerStatuses', []))
            
            if ready:
                self.status_label.setText("Status: Running ✓")
                self.status_label.setStyleSheet(f"color: {self.color}; font-size: 14px; font-weight: bold;")
            else:
                self.status_label.setText(f"Status: {status}")
                self.status_label.setStyleSheet("color: #ff0000; font-size: 14px;")
            
            # Metrics
            if metrics:
                cpu = metrics['cpu']
                memory = metrics['memory']
                
                self.cpu_label.setText(f"CPU: {cpu}m")
                self.cpu_progress.setValue(min(100, cpu // 10))  # 1000m = 100%
                
                self.memory_label.setText(f"Memory: {memory}Mi")
                self.memory_progress.setValue(min(100, memory // 10))  # 1000Mi = 100%
            
            # Pod info
            self.pod_info.setText(f"Pod: {pod_data['metadata']['name']}")
        else:
            self.status_label.setText("Status: Not Found")
            self.status_label.setStyleSheet("color: #666; font-size: 14px;")

class ConnectionMap(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(350)
        self.animation_offset = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(50)
        
        # Connection states
        self.gateway_meta_ok = True
        self.meta_redis_ok = False
        self.redis_districts_ok = False
    
    def animate(self):
        self.animation_offset = (self.animation_offset + 2) % 20
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background with grid
        painter.fillRect(self.rect(), QColor(0, 0, 0, 240))
        painter.setPen(QPen(QColor(0, 255, 0, 20), 1))
        for i in range(0, self.width(), 20):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height(), 20):
            painter.drawLine(0, i, self.width(), i)
        
        # Draw connection diagram
        width = self.width()
        height = self.height()
        
        # Gateway with glow effect
        gateway_rect = QRect(width//2 - 100, 20, 200, 70)
        
        # Outer glow
        glow_pen = QPen(QColor(255, 255, 0, 50), 6)
        painter.setPen(glow_pen)
        painter.drawRoundedRect(gateway_rect.adjusted(-3, -3, 3, 3), 10, 10)
        
        # Main rect
        painter.setPen(QPen(QColor(255, 255, 0), 3))
        painter.setBrush(QBrush(QColor(255, 255, 0, 20)))
        painter.drawRoundedRect(gateway_rect, 10, 10)
        
        # Text
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        painter.drawText(gateway_rect, Qt.AlignmentFlag.AlignCenter, "GATEWAY\n:30889\n[NGINX]")
        
        # Status indicator
        status_rect = QRect(gateway_rect.right() - 20, gateway_rect.top() + 5, 15, 15)
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(status_rect)
        
        # Meta-Chain (orchestrator) with animation
        meta_rect = QRect(width//2 - 100, 110, 200, 70)
        
        # Animated border
        gradient = QLinearGradient(meta_rect.topLeft(), meta_rect.bottomRight())
        gradient.setColorAt(0, QColor(0, 255, 255, 150))
        gradient.setColorAt(0.5, QColor(0, 150, 255, 150))
        gradient.setColorAt(1, QColor(0, 255, 255, 150))
        
        painter.setPen(QPen(QBrush(gradient), 3))
        painter.setBrush(QBrush(QColor(0, 255, 255, 20)))
        painter.drawRoundedRect(meta_rect, 10, 10)
        
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        painter.drawText(meta_rect, Qt.AlignmentFlag.AlignCenter, "META-CHAIN\n[Elixir Brain]\nOrchestrator")
        
        # CPU indicator
        cpu_rect = QRect(meta_rect.right() - 50, meta_rect.bottom() - 25, 45, 20)
        painter.setBrush(QBrush(QColor(0, 255, 255, 40)))
        painter.setPen(QPen(QColor(0, 255, 255), 1))
        painter.drawRect(cpu_rect)
        painter.drawText(cpu_rect, Qt.AlignmentFlag.AlignCenter, "75Mi")
        
        # Connection Gateway -> Meta-Chain (animated flow)
        if self.gateway_meta_ok:
            # Draw animated data packets
            painter.setPen(QPen(QColor(0, 255, 0), 3))
            painter.drawLine(width//2, 90, width//2, 110)
            
            # Animated packets
            for i in range(3):
                y = 90 + ((self.animation_offset + i * 7) % 20)
                if y < 110:
                    painter.setBrush(QBrush(QColor(0, 255, 0)))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(QPoint(width//2, y), 4, 4)
            
            # Connection label
            painter.setPen(QPen(QColor(0, 255, 0), 1))
            painter.drawText(width//2 + 10, 100, "HTTP/WS ✓")
        
        # Redis with error effect
        redis_rect = QRect(width//2 - 80, 210, 160, 60)
        
        # Error glow
        error_alpha = 100 + int(50 * abs(self.animation_offset - 10) / 10)
        painter.setPen(QPen(QColor(255, 0, 0, error_alpha), 4))
        painter.setBrush(QBrush(QColor(255, 0, 0, 10)))
        painter.drawRoundedRect(redis_rect, 10, 10)
        
        # Main rect
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.DashLine))
        painter.drawRoundedRect(redis_rect, 10, 10)
        
        painter.setPen(QPen(QColor(255, 100, 100), 1))
        painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        painter.drawText(redis_rect, Qt.AlignmentFlag.AlignCenter, "REDIS\n10.43.94.110:6379\n⚠️ ENETUNREACH")
        
        # Error icon
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawText(redis_rect.right() - 25, redis_rect.top() + 20, "✗")
        
        # Connection Meta-Chain -> Redis (broken with spark effect)
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.DashLine))
        painter.drawLine(width//2, 180, width//2, 210)
        
        # Spark effect at break point
        spark_y = 195
        painter.setPen(QPen(QColor(255, 100, 0), 1))
        for angle in range(0, 360, 45):
            import math
            x = width//2 + 10 * math.cos(math.radians(angle + self.animation_offset * 5))
            y = spark_y + 10 * math.sin(math.radians(angle + self.animation_offset * 5))
            painter.drawLine(width//2, spark_y, x, y)
        
        painter.setPen(QPen(QColor(255, 0, 0), 1))
        painter.drawText(width//2 + 15, 195, "Pub/Sub ✗")
        
        # Other Districts with tech stack labels
        districts = [
            ("PATTERN\nDISTRICT", "[Rust]", 150, 300, QColor(255, 0, 255)),
            ("MEMORY\nQUARTER", "[Go]", 350, 300, QColor(0, 255, 0)),
            ("INTELLIGENCE\nHUB", "[Python]", 550, 300, QColor(255, 128, 0)),
            ("GATEWAY\nDISTRICT", "[Future]", 750, 300, QColor(100, 100, 255))
        ]
        
        for name, tech, x, y, color in districts:
            if x > width - 100:
                continue
                
            rect = QRect(x - 60, y, 120, 70)
            
            # Faded effect for non-connected
            painter.setPen(QPen(color.darker(150), 2, Qt.PenStyle.DashLine))
            painter.setBrush(QBrush(QColor(color.red(), color.green(), color.blue(), 20)))
            painter.drawRoundedRect(rect, 10, 10)
            
            painter.setPen(QPen(color.lighter(150), 1))
            painter.setFont(QFont('Arial', 9))
            painter.drawText(rect.adjusted(0, 5, 0, 0), Qt.AlignmentFlag.AlignHCenter, name)
            painter.setFont(QFont('Arial', 8))
            painter.drawText(rect.adjusted(0, 0, 0, -5), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, tech)
            
            # Draw broken connection from Redis to Districts
            painter.setPen(QPen(QColor(255, 0, 0, 50), 1, Qt.PenStyle.DashLine))
            painter.drawLine(x, y, width//2, 270)
            
            # Status indicator
            status_rect = QRect(rect.right() - 20, rect.top() + 5, 15, 15)
            painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(status_rect)
        
        # Info box
        info_rect = QRect(10, height - 80, 300, 70)
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))
        painter.drawRoundedRect(info_rect, 5, 5)
        
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont('Consolas', 9))
        painter.drawText(info_rect.adjusted(10, 10, -10, -10), 
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                        "ISSUE: Redis ENETUNREACH\n"
                        "Gateway → Meta-Chain ✓\n"
                        "Meta-Chain → Redis ✗\n"
                        "Redis → Districts ✗")

class CRODDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.districts = {}
        self.init_ui()
        
        # Start metrics worker
        self.worker = MetricsWorker()
        self.worker.metrics_updated.connect(self.update_metrics)
        self.worker.start()
    
    def init_ui(self):
        self.setWindowTitle("CROD POLYGLOT CITY - Live Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #000;
            }
            QLabel {
                color: #0f0;
            }
        """)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel("🏙️ CROD POLYGLOT CITY - LIVE METRICS")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #0ff;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00ff00, stop:0.5 #00ffff, stop:1 #ff00ff);
            background-clip: text;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Status bar
        self.status_label = QLabel("Connecting to K8s...")
        self.status_label.setStyleSheet("color: #ff0; padding: 10px;")
        main_layout.addWidget(self.status_label)
        
        # Connection Map
        self.connection_map = ConnectionMap()
        main_layout.addWidget(self.connection_map)
        
        # Districts grid
        districts_layout = QGridLayout()
        
        district_configs = [
            ("meta-chain", "Meta-Chain (Elixir)", "#00ffff"),
            ("pattern-district", "Pattern District (Rust)", "#ff00ff"),
            ("memory-quarter", "Memory Quarter (Go)", "#00ff00"),
            ("intelligence-hub", "Intelligence Hub (Python)", "#ff8800")
        ]
        
        for i, (key, name, color) in enumerate(district_configs):
            widget = DistrictWidget(name, color)
            self.districts[key] = widget
            districts_layout.addWidget(widget, i // 2, i % 2)
        
        main_layout.addLayout(districts_layout)
        
        # CPU/Memory graphs
        self.init_graphs()
        main_layout.addWidget(self.graph_widget)
        
        central.setLayout(main_layout)
    
    def init_graphs(self):
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_widget.setBackground('k')
        self.graph_widget.setMinimumHeight(200)
        
        # CPU graph
        self.cpu_plot = self.graph_widget.addPlot(title="CPU Usage Over Time")
        self.cpu_plot.setLabel('left', 'CPU', units='m')
        self.cpu_plot.setLabel('bottom', 'Time', units='s')
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.3)
        
        self.cpu_curves = {}
        colors = ['c', 'm', 'g', 'y']
        for i, key in enumerate(self.districts.keys()):
            self.cpu_curves[key] = self.cpu_plot.plot(pen=colors[i % len(colors)])
        
        self.cpu_data = {key: [] for key in self.districts}
        self.time_data = []
    
    def update_metrics(self, data):
        self.status_label.setText(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        pods = {pod['metadata']['name']: pod for pod in data['pods']}
        metrics = data['metrics']
        
        # Update each district
        for key, widget in self.districts.items():
            # Find matching pod
            pod_data = None
            pod_metrics = None
            
            for pod_name, pod in pods.items():
                if key in pod_name:
                    pod_data = pod
                    pod_metrics = metrics.get(pod_name)
                    break
            
            widget.update_metrics(pod_data, pod_metrics)
            
            # Update graph data
            if pod_metrics:
                self.cpu_data[key].append(pod_metrics['cpu'])
                if len(self.cpu_data[key]) > 50:  # Keep last 50 points
                    self.cpu_data[key].pop(0)
        
        # Update time
        if self.cpu_data[list(self.districts.keys())[0]]:
            self.time_data = list(range(len(self.cpu_data[list(self.districts.keys())[0]])))
        
        # Update graphs
        for key, curve in self.cpu_curves.items():
            if self.cpu_data[key]:
                curve.setData(self.time_data, self.cpu_data[key])

def main():
    app = QApplication(sys.argv)
    
    # Dark theme
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    
    dashboard = CRODDashboard()
    dashboard.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()