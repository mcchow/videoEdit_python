import gdown

url = 'https://drive.google.com/uc?id=1x_BkzZqBO3mEvxXj7s_Hcyf94sL7g7z5'
output = 'D:/github/videoEdit_python/videoK.mp4'  # Add the appropriate file extension
gdown.download(url, output, quiet=False)