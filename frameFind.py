import cv2
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error


def find_frame_time(image_path, video_path,threshold=0.9):
    # intial value
    sec_to_skip = 3
    start_time=0
    end_time=0
    start_image = cv2.imread(image_path)

    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(total_frames)
    fps= int(cap.get(cv2.CAP_PROP_FPS))
    print(fps)
    # Set the frame position to the beginning
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Define a variable to store the frame number
    current_frame = fps*20*60

    #find start time
    while current_frame < total_frames:
        # Read a frame
        ret, frame = cap.read()
        

        # Check if the frame was read successfully
        if not ret:
            break

        # Process the frame (you can save it, display it, etc.)
        gray_start_image = cv2.cvtColor(start_image, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the percentage of the video processed
        percentage_processed = ((cap.get(cv2.CAP_PROP_POS_FRAMES) / total_frames) * 100)
        print(f"Percentage processed: {percentage_processed:.2f}%")
        # Calculate SSIM
        
        
        # Calculate SSIM
        ssim_value, _ = ssim(gray_start_image, gray_image2, full=True)
        print(f"SSIM: {ssim_value}")
        if ssim_value>=0.99:
            match_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert milliseconds to seconds
            print(f"Template found at {match_time} seconds")
            start_time=match_time
            break
        

        # Increment the frame counter
        current_frame += fps*sec_to_skip

        # Set the frame position to the next 1000th frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    current_frame += fps*20*60
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    # find end time
    while current_frame < total_frames:
        # Read a frame
        ret, frame = cap.read()
        

        # Check if the frame was read successfully
        if not ret:
            break

        # Process the frame (you can save it, display it, etc.)
        gray_image2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the percentage of the video processed
        percentage_processed = ((cap.get(cv2.CAP_PROP_POS_FRAMES) / total_frames) * 100)
        print(f"Percentage processed: {percentage_processed:.2f}%")
        # Calculate SSIM
        
        
        # Calculate SSIM
        ssim_value, _ = ssim(gray_start_image, gray_image2, full=True)
        print(f"SSIM: {ssim_value}")
        if ssim_value>=threshold:
            match_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Convert milliseconds to seconds
            print(f"Template found at {match_time} seconds")
            end_time=match_time
            break
        

        # Increment the frame counter
        current_frame += fps*sec_to_skip

        # Set the frame position to the next 1000th frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        print(cap.get(cv2.CAP_PROP_POS_FRAMES))
    #/////////////////////////////////



    return start_time,end_time
    # Release the video capture object
    cap.release()

# Example usage
image_path = r'D:\github\videoEdit_python\image\start.png'  # Path to the captured frame
video_path = 'video\ecc.mp4'  # Path to the target video
threshold = 0.7  # Adjust the threshold based on your needs

find_frame_time(image_path, video_path, threshold)
#trim_video(input_video_path, output_video_path, start_time, end_time)