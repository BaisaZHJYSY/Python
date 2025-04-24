from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QLineEdit, QPushButton, QTextEdit, 
                            QProgressBar)
from PyQt5.QtCore import QThread, pyqtSignal
from bilibili import download_bilibili_video
import sys

class DownloadThread(QThread):
    """ 下载线程（防止界面卡死） """
    progress_signal = pyqtSignal(int)  # 进度信号
    finish_signal = pyqtSignal(bool)   # 完成信号

    def __init__(self, bv_id):
        super().__init__()
        self.bv_id = bv_id

    def run(self):
        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    percent = int(float(d['_percent_str'].strip('%')))
                    self.progress_signal.emit(percent)

            output_dir = 'downloads'
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                'progress_hooks': [progress_hook],
                'quiet': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://www.bilibili.com/video/{self.bv_id}'])
            
            self.finish_signal.emit(True)
        except Exception:
            self.finish_signal.emit(False)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B站视频下载器")
        self.setGeometry(100, 100, 500, 400)
        
        # 主布局
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 输入区域
        layout.addWidget(QLabel("BV号:"))
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("例如：BV1GJ411x7h7")
        layout.addWidget(self.entry)
        
        # 下载按钮
        self.btn = QPushButton("下载")
        self.btn.clicked.connect(self.start_download)
        layout.addWidget(self.btn)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        
        # 日志输出
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def start_download(self):
        bv_id = self.entry.text().strip()
        if not bv_id.startswith("BV"):
            self.log.append("错误：请输入有效的BV号（以BV开头）")
            return
        
        self.btn.setEnabled(False)
        self.progress.setValue(0)
        self.log.append(f"开始下载 {bv_id}...")
        
        # 启动下载线程
        self.thread = DownloadThread(bv_id)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.finish_signal.connect(self.download_finished)
        self.thread.start()
    
    def update_progress(self, percent):
        """ 更新进度条 """
        self.progress.setValue(percent)
        if percent == 100:
            self.log.append("视频处理中...")
    
    def download_finished(self, success):
        """ 下载完成处理 """
        self.btn.setEnabled(True)
        if success:
            self.log.append("下载完成！")
        else:
            self.log.append("下载失败，请检查控制台")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())