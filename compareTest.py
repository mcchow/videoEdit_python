import cv2
from skimage.metrics import structural_similarity as ssim

image_path = r'image\start.png'  # Path to the captured frame
video_path = 'input.mp4'  # Path to the target video
threshold = 0.7  # Adjust the threshold based on your needs
capture_time=5614

cap = cv2.VideoCapture(video_path)

start_image = cv2.imread(image_path)
start_image2 = start_image[:start_image.shape[0]//8, :,:]

# Set the capture time in seconds
cap.set(cv2.CAP_PROP_POS_MSEC, capture_time * 1000)
# Read the frame at the specified time
ret, frame = cap.read()
image2 = frame[:frame.shape[0]//8, :]
print(image2.shape)
print(start_image2.shape)
cv2.imshow('Current Frame', image2)

cv2.waitKey(0)  # Add this line
cv2.destroyAllWindows()  # And this line

ssim_value, _ = ssim(start_image2, image2, full=True , win_size=3)
print(f"SSIM: {ssim_value}")