from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap
from cutframe import *
from cutvideo import *
import sys
import os




class MyApp(QWidget):
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


        self.initUI()

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
        vbox.addWidget(QLabel("Start:"))
        vbox.addWidget(self.start)
        vbox.addWidget(QLabel("End:"))
        vbox.addWidget(self.end)
        downloadBtn = QPushButton('Download', self)
        vbox.addWidget(downloadBtn)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())