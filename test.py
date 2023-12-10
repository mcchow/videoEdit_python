import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error

def compare_frames(image_path, video_path):
    image2 = cv2.imread(image_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Set the capture time in seconds
    cap.set(cv2.CAP_PROP_POS_MSEC, 1861 * 1000)

    # Read the frame at the specified time
    ret, frame = cap.read()

    # Convert images to grayscale for SSIM comparison
    gray_image1 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    ssim_value, _ = ssim(gray_image1, gray_image2, full=True)

    # Calculate Mean Squared Error (MSE)
    mse_value = mean_squared_error(frame.flatten(), image2.flatten())

    # Release the video capture object
    cap.release()
    return ssim_value, mse_value

if __name__ == "__main__":
    image_path = 'D:/github/videoEdit_python/image/start.png'
    video_path = 'D:/github/videoEdit_python/video/ecc.mp4'
    
    differences = compare_frames(image_path, video_path)
    
    print("List of differences for each frame:", differences)