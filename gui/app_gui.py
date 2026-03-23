import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import pyqtgraph as pg

from monitor.ssh_monitor import get_stats
from alerts import send_alert
from config.settings import SERVER, CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD


# ================= GLASS CARD ================= #

class GlassCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QFrame{
            background: rgba(255,255,255,0.05);
            border-radius:18px;
            border:1px solid rgba(255,255,255,0.12);
        }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setOffset(0,8)
        shadow.setColor(QColor(0,0,0,160))

        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20,20,20,20)


# ================= CIRCULAR METER ================= #

class CircularMeter(QWidget):

    def __init__(self):
        super().__init__()
        self.value = 0
        self.setMinimumSize(180,180)

    def set_value(self, val):
        self.value = val
        self.update()

    def paintEvent(self, e):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(15,15,-15,-15)

        # background
        painter.setPen(QPen(QColor(70,70,70), 14))
        painter.drawArc(rect, 0, 360*16)

        # dynamic color
        color = QColor(0,255,170) if self.value < 70 else QColor(255,165,0) if self.value < 85 else QColor(255,60,60)

        painter.setPen(QPen(color, 14))
        painter.drawArc(rect, 90*16, int(-self.value * 3.6 * 16))

        painter.setFont(QFont("Segoe UI", 16, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value:.0f}%")


# ================= THREAD ================= #

class MonitorThread(QThread):

    data_signal = pyqtSignal(float, float, float, str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.last_alert = 0

    def run(self):

        while self.running:

            cpu, ram, disk = get_stats()

            msg = f"""
🚨 SERVER HEALTH REPORT

Server : {SERVER['name']}

CPU Usage : {cpu:.2f}% (Limit {CPU_THRESHOLD}%)
RAM Usage : {ram:.2f}% (Limit {RAM_THRESHOLD}%)
Disk Usage : {disk:.2f}% (Limit {DISK_THRESHOLD}%)

-----------------------------
"""

            self.data_signal.emit(cpu, ram, disk, msg)

            now = time.time()

            # prevent alert spam
            if now - self.last_alert > 60:

                if cpu > CPU_THRESHOLD:
                    send_alert(
                        "🚨 High CPU Usage!",
                        f"""
Your server is currently using {cpu:.2f}% CPU.

Safe limit is {CPU_THRESHOLD}%  
This may slow down applications.

Recommended:
✔ Stop heavy tasks  
✔ Check background processes  
✔ Scale server if needed
"""
                    )

                elif ram > RAM_THRESHOLD:
                    send_alert(
                        "🚨 High RAM Usage!",
                        f"""
Memory usage reached {ram:.2f}%.

Safe limit is {RAM_THRESHOLD}%.

Recommended:
✔ Close memory-heavy apps  
✔ Clear cache  
✔ Upgrade RAM if frequent
"""
                    )

                self.last_alert = now

            self.msleep(2000)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


# ================= GUI ================= #

class ServerMonitorGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("⚡ Ultra Server Monitor")
        self.resize(1200,700)

        self.setStyleSheet("""
        QWidget{
            background:qlineargradient(
                x1:0,y1:0,x2:1,y2:1,
                stop:0 #0f2027,
                stop:0.5 #203a43,
                stop:1 #2c5364
            );
            color:white;
            font-size:13px;
        }
        """)

        main_layout = QHBoxLayout(self)

        # ================= SIDEBAR ================= #

        sidebar = QVBoxLayout()

        title = QLabel("🚀 Monitor")
        title.setFont(QFont("Segoe UI",18,QFont.Bold))

        self.status = QLabel("● Stopped")
        self.status.setStyleSheet("color:red;")

        start_btn = QPushButton("Start")
        stop_btn = QPushButton("Stop")

        start_btn.setStyleSheet("background:#00c853;padding:10px;border-radius:8px;")
        stop_btn.setStyleSheet("background:#d50000;padding:10px;border-radius:8px;")

        # logs
        log_title = QLabel("📜 Live Logs")
        log_title.setFont(QFont("Segoe UI",11,QFont.Bold))

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setMaximumWidth(260)
        self.logs.setStyleSheet("""
        background:rgba(0,0,0,0.35);
        border-radius:10px;
        """)

        sidebar.addWidget(title)
        sidebar.addWidget(self.status)
        sidebar.addSpacing(10)
        sidebar.addWidget(start_btn)
        sidebar.addWidget(stop_btn)
        sidebar.addSpacing(20)
        sidebar.addWidget(log_title)
        sidebar.addWidget(self.logs)
        sidebar.addStretch()

        main_layout.addLayout(sidebar,1)

        # ================= DASHBOARD ================= #

        dashboard = QVBoxLayout()
        meters_layout = QHBoxLayout()

        # CPU CARD
        cpu_card = GlassCard()

        cpu_title = QLabel("CPU Meter")
        cpu_title.setAlignment(Qt.AlignCenter)
        cpu_title.setFont(QFont("Segoe UI",11,QFont.Bold))

        self.cpu_meter = CircularMeter()

        cpu_card.layout.addWidget(cpu_title)
        cpu_card.layout.addWidget(self.cpu_meter)

        # RAM CARD
        ram_card = GlassCard()

        ram_title = QLabel("RAM Meter")
        ram_title.setAlignment(Qt.AlignCenter)
        ram_title.setFont(QFont("Segoe UI",11,QFont.Bold))

        self.ram_meter = CircularMeter()

        ram_card.layout.addWidget(ram_title)
        ram_card.layout.addWidget(self.ram_meter)

        meters_layout.addWidget(cpu_card)
        meters_layout.addWidget(ram_card)

        dashboard.addLayout(meters_layout)

        # ===== GRAPHS ===== #

        self.cpu_graph = pg.PlotWidget()
        self.cpu_graph.setBackground((0,0,0,0))
        self.cpu_line = self.cpu_graph.plot(pen=pg.mkPen('#00ffea',width=2))

        self.ram_graph = pg.PlotWidget()
        self.ram_graph.setBackground((0,0,0,0))
        self.ram_line = self.ram_graph.plot(pen=pg.mkPen('#ff6ec7',width=2))

        dashboard.addWidget(self.cpu_graph)
        dashboard.addWidget(self.ram_graph)

        main_layout.addLayout(dashboard,4)

        # ===== THREAD ===== #

        self.thread=None
        self.cpu_data=[]
        self.ram_data=[]

        start_btn.clicked.connect(self.start)
        stop_btn.clicked.connect(self.stop)

    # ================= START ================= #

    def start(self):

        if self.thread and self.thread.isRunning():
            return

        self.status.setText("● Running")
        self.status.setStyleSheet("color:#00e676;")

        self.thread=MonitorThread()
        self.thread.data_signal.connect(self.update_ui)
        self.thread.start()

    # ================= STOP ================= #

    def stop(self):

        if self.thread:
            self.thread.stop()
            self.thread=None

        self.status.setText("● Stopped")
        self.status.setStyleSheet("color:red;")

    # ================= UPDATE UI ================= #

    def update_ui(self,cpu,ram,disk,msg):

        self.cpu_meter.set_value(cpu)
        self.ram_meter.set_value(ram)

        self.logs.append(msg)

        self.logs.verticalScrollBar().setValue(
            self.logs.verticalScrollBar().maximum()
        )

        self.cpu_data.append(cpu)
        self.ram_data.append(ram)

        self.cpu_data=self.cpu_data[-50:]
        self.ram_data=self.ram_data[-50:]

        self.cpu_line.setData(self.cpu_data)
        self.ram_line.setData(self.ram_data)
