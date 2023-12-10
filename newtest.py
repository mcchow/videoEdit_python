import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error

def trim_video(input_path, output_path, start_time, end_time):
    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Get the original video's properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(5)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs as well
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Set the video capture to the desired start time
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_time * fps))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret or cap.get(cv2.CAP_PROP_POS_FRAMES) > int(end_time * fps):
            break

        # Write the frame to the output video
        out.write(frame)

        # Display the frame (optional)
        cv2.imshow('Trimmed Frame', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Close all windows
    cv2.destroyAllWindows()

import cv2
import numpy as np

def find_frame_time(image_path, video_path, threshold=0.7):
    pre = -1
    # Load the captured frame as a template
    image1 = cv2.imread(image_path)

    # Read the target video
    cap = cv2.VideoCapture(video_path)
    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(total_frames)
    
    compressed_frames = []

    # Calculate the delay in milliseconds for capturing one frame per second
    delay = 1000
    print(delay)
    current_frame=0
    # Iterate through the frames in the video
    while current_frame < total_frames:
        cap.set(cv2.CAP_PROP_POS_MSEC, current_frame)
        # Calculate the current frame number
        current_frame = current_frame+delay
        ret, frame = cap.read()

        if not ret:
            break

        # Convert images to grayscale for SSIM comparison
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Current Frame', frame)
        # Print the middle element (pixel) of the frame
        height, width, channels = frame.shape
        middle_pixel = frame[height // 2, width // 2]
        print(f"Middle Pixel Value: {middle_pixel}")
        # Calculate SSIM
        ssim_value, _ = ssim(gray_image1, gray_image2, full=True)

        # Calculate the percentage of the video processed
        percentage_processed = ((current_frame / total_frames) * 100)
        if pre != percentage_processed:
            print(f"Percentage processed: {percentage_processed:.2f}%")
            print(f"SSIM: {ssim_value:.2f}%")
            pre=percentage_processed
        

        # If enough good matches are found, consider the frame as a match
        if ssim_value>=0.9:
            match_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert milliseconds to seconds
            print(f"Template found at {match_time} seconds")
            break


    # Release the video capture object
    cap.release()

# Example usage
image_path = r'D:\github\videoEdit_python\image\start.png'  # Path to the captured frame
video_path = 'video\ecc.mp4'  # Path to the target video
threshold = 0.95  # Adjust the threshold based on your needs

print(find_frame_time(image_path, video_path, threshold))
#trim_video(input_video_path, output_video_path, start_time, end_time)