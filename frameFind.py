import cv2
from skimage.metrics import structural_similarity as ssim


def find_frame_time(image_path, video_path,threshold=0.9,signal=None):
    # intial value
    sec_to_skip = 1
    start_time=0
    end_time=0
    start_image = cv2.imread(image_path)
    gray_start_image = start_image[:start_image.shape[0]//2, :]

    #
    #
    #
    start_image2 = start_image[:start_image.shape[0]//8, :]
    pre =0


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
        gray_image2 = frame[:frame.shape[0]//2, :]

        # Calculate the percentage of the video processed
        percentage_processed = ((cap.get(cv2.CAP_PROP_POS_FRAMES) / total_frames) * 100)
        if signal is not None:
            #return progess
            if(pre != int(percentage_processed)):
                pre = int(percentage_processed)
                signal.emit(pre)
        print(f"Percentage processed start: {percentage_processed:.2f}%")
        # Calculate SSIM
        
        
        # Calculate SSIM
        ssim_value, _ = ssim(gray_start_image, gray_image2, full=True, win_size=3)
        print(f"SSIM: {ssim_value}")
        if ssim_value>=0.96:
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
        image2 = frame[:frame.shape[0]//8, :]

        # Calculate the percentage of the video processed
        percentage_processed = ((cap.get(cv2.CAP_PROP_POS_FRAMES) / total_frames) * 100)
        if signal is not None:
            #update progress bar
            if(pre != int(percentage_processed)):
                pre = int(percentage_processed)
                signal.emit(pre)
        print(f"Percentage processed end: {percentage_processed:.2f}%")
        # Calculate SSIM
        
        
        # Calculate SSIM
        ssim_value, _ = ssim(start_image2, image2, full=True, win_size=3)
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

    # Release the video capture object
    cap.release()
    signal.emit(100)
    return start_time,end_time
    

# Example usage
'''
image_path = r'D:\github\videoEdit_python\image\start.png'  # Path to the captured frame
video_path = 'input.mp4'  # Path to the target video
threshold = 0.7  # Adjust the threshold based on your needs

find_frame_time(image_path, video_path, threshold)
'''


