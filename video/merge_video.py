from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile
import io

def merge_videos(video_paths, output_path="merged_video.mp4"):
    """
    Merges a list of video files into a single video.

    :param video_paths: List of paths to video files.
    :param output_path: Path to save the merged video.
    """
    try:
        clips = [VideoFileClip(video) for video in video_paths]
        final_clip = concatenate_videoclips(clips, method="compose")
        # final_clip.write_videofile(output_path, codec="libx264", fps=24)
        # print(f"Merged video saved as: {output_path}")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_path = temp_file.name
        temp_file.close()  # Close so moviepy can write to it
        final_clip.write_videofile(temp_path, codec="libx264", audio_codec="aac", fps=30)

        video_io = io.BytesIO()
        with open(temp_path, "rb") as f:
            video_io.write(f.read())
        video_io.seek(0)
        return video_io

        # return output_path
    except Exception as e:
        print(f"Error: {e}")
    finally:
        for clip in clips:
            clip.close()
