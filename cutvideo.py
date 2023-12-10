from moviepy.video.io.VideoFileClip import VideoFileClip

def cut_video(input_path, output_path, start_time, end_time):
    # Load the video clip
    video_clip = VideoFileClip(input_path)

    # Cut the video from start_time to end_time
    cut_clip = video_clip.subclip(start_time, end_time)

    # Write the cut video to the output file
    cut_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close the video clip
    video_clip.close()

# Example usage
'''
input_video_path = "input.mp4"
output_video_path = "output_video.mp4"
start_time = 10  # Start time in seconds
end_time = 30    # End time in seconds

cut_video(input_video_path, output_video_path, start_time, end_time)
'''
