from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap
from cutframe import *
from cutvideo import *
from downloadVideo import *
from frameFind import *
import importlib.util
import sys
import os
import subprocess
import gdown



class MyApp(QWidget):
    progress_signal = pyqtSignal(int)
    progress_signal2 = pyqtSignal(int)
    def __init__(self):
        super().__init__()

        self.url_input = QLineEdit(self)
        self.start = QLineEdit(self)
        self.end = QLineEdit(self)
        self.image1 = QLabel(self)
        self.image2 = QLabel(self)
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.Output_dest = QLineEdit(self)
        self.Output_dest.setText(current_folder+'\output.mp4')
        self.file_dest = QLineEdit(self)
        self.file_dest.setText(current_folder+'\input.mp4')
        self.progress_bar = QProgressBar(self)
        self.get_time_progress_bar = QProgressBar(self)


        self.initUI()

    def on_download_clicked(self):
        try:
            url_text = self.url_input.text()
            video_path = self.file_dest.text()
            if url_text and video_path:
                '''
                folder_name = os.path.dirname(video_path)
                file_name = os.path.basename(video_path)
                download_youtube_video(url_text,folder_name,file_name, self.progress_signal)
                '''
                
                gdown.download(url_text, video_path, quiet=False)
            
        except:
            print('something missing')
    
    @pyqtSlot(int)
    def on_progress(self, progress):
        self.progress_bar.setValue(progress)

    def on_get_time_clicked(self):
        try:
            script_directory = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to 'start.png' in the 'image' directory
            image_path = os.path.join(script_directory, 'image', 'start.png')
            print(image_path)
            video_path = self.file_dest.text()
            if video_path:
                start_time,end_time=find_frame_time(image_path, video_path,0.9,self.progress_signal2)
                self.start.setText(str((int)(start_time)))
                self.end.setText(str((int)(end_time)))
            
        except:
            print('something missing')
    
    @pyqtSlot(int)
    def on_get_time_progress(self, progress):
        self.get_time_progress_bar.setValue(progress)
    
    def on_view_clicked(self):
        try:
            video_path = self.file_dest.text()
            start_text = self.start.text()
            end_text = self.end.text()
            if start_text:
                start_time = int(start_text)  # Time in seconds
                qpixmap=capture_frame_qimage(video_path,start_time)
                self.image1.setPixmap(qpixmap)
            if end_text:
                start_time = int(end_text) # Time in seconds
                qpixmap=capture_frame_qimage(video_path,start_time)
                self.image2.setPixmap(qpixmap)
            
        except:
            print('something missing')
    
    def on_crop_clicked(self):
        video_path = self.file_dest.text()
        result_dest = self.Output_dest.text()
        start_text = self.start.text()
        end_text = self.end.text()

        if not video_path or not start_text or not end_text or not result_dest:
            print("Error: Start and end inputs cannot be empty.")
            return

        try:
            start = int(start_text)
            end = int(end_text)
            cut_video(video_path, result_dest, start, end)

        except ValueError:
            print("Error: Start and end inputs must be numbers.")
            return


    def initUI(self):
        self.setAcceptDrops(True)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("URL:"))
        vbox.addWidget(self.url_input)
        vbox.addWidget(QLabel("File Location/Destination:"))
        vbox.addWidget(self.file_dest)
        downloadBtn = QPushButton('Download', self)
        downloadBtn.clicked.connect(self.on_download_clicked)
        vbox.addWidget(downloadBtn)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(QLabel("Start:"))
        vbox.addWidget(self.start)
        vbox.addWidget(QLabel("End:"))
        vbox.addWidget(self.end)
        
        AutoCropBtn = QPushButton('Auto Set Time', self)
        AutoCropBtn.clicked.connect(self.on_get_time_clicked)
        vbox.addWidget(AutoCropBtn)
        vbox.addWidget(self.get_time_progress_bar)
        viewBtn = QPushButton('View', self)
        vbox.addWidget(viewBtn)
        viewBtn.clicked.connect(self.on_view_clicked)
        vbox.addWidget(QLabel("Start:"))
        vbox.addWidget(self.image1)
        vbox.addWidget(QLabel("End:"))
        vbox.addWidget(self.image2)
        vbox.addWidget(QLabel("Output Location/Destination:"))
        vbox.addWidget(self.Output_dest)
        cropBtn = QPushButton('Crop', self)
        cropBtn.clicked.connect(self.on_crop_clicked)
        vbox.addWidget(cropBtn)

        self.setLayout(vbox)

        self.setWindowTitle('My App')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            self.file_dest.setText(path)

def check_installation(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"{package_name} is not installed.")
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return False
    else:
        print(f"{package_name} is installed.")
        return True

# List of packages to check
packages = ["cv2", "numpy", "pyqt5", "gdown" , "moviepy","scikit-learn"]

# Check each package
for package in packages:
    check_installation(package)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.progress_signal.connect(ex.on_progress)
    ex.progress_signal2.connect(ex.on_get_time_progress)
    sys.exit(app.exec_())