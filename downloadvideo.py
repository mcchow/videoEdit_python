from pytube import YouTube, Stream
import os

def progress_function(stream: Stream, chunk: bytes, bytes_remaining: int, signal):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = (bytes_downloaded / total_size) * 100
    signal.emit(int(liveprogress))

def download_youtube_video(video_url, output_path='path/to/save', new_filename='ecc.mp4', signal=None):
    try:
        # Create a YouTube object
        youtube = YouTube(video_url)

        # Register the progress callback function
        if signal is not None:
            youtube.register_on_progress_callback(lambda stream, chunk, bytes_remaining: progress_function(stream, chunk, bytes_remaining, signal))

        # Get the highest resolution stream
        video_stream = youtube.streams.get_highest_resolution()

        # Download the video with the specified filename
        video_file_path = os.path.join(output_path, new_filename)
        video_stream.download(output_path, filename=new_filename)

        print(f"Video downloaded successfully as: {video_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
'''
youtube_url = 'https://www.youtube.com/watch?v=bPs_3B8bk-Q&ab_channel=EvangelicalChineseChurchofSeattle%E8%A5%BF%E9%9B%85%E5%9C%96%E8%AD%89%E9%81%93%E5%A0%82'
output_path = 'video'

download_youtube_video(youtube_url, output_path)
'''
