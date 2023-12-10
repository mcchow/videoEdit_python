import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

def capture_frame(video_path, output_image_path, capture_time):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Set the capture time in seconds
    cap.set(cv2.CAP_PROP_POS_MSEC, capture_time * 1000)

    # Read the frame at the specified time
    ret, frame = cap.read()
    cv2.imshow('Current Frame', frame)
    # Check if the frame is read successfully
    if ret:
        # Save the frame as an image file
        cv2.imwrite(output_image_path, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        print(f"Frame captured at {capture_time} seconds and saved as {output_image_path}")
    else:
        print(f"Failed to capture frame at {capture_time} seconds")

    # Release the video capture object
    cap.release()

def capture_frame_qimage(video_path, capture_time):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Set the capture time in seconds
    cap.set(cv2.CAP_PROP_POS_MSEC, capture_time * 1000)

    # Read the frame at the specified time
    ret, frame = cap.read()
    # Check if the frame is read successfully
    if ret:
        # Save the frame as an image file
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create QImage from the frame
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qimage = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # Create QPixmap from QImage
        qpixmap = QPixmap.fromImage(qimage)
    else:
        print(f"Failed to capture frame at {capture_time} seconds")

    # Release the video capture object
    cap.release()
    qpixmap = qpixmap.scaled(400, 400, Qt.KeepAspectRatio)
    return qpixmap


# Example usage
'''
video_path = 'video\ecc.mp4'
output_image_path = 'image\start.png'
capture_time = 1861  # Time in seconds

capture_frame(video_path, output_image_path, capture_time)
'''
