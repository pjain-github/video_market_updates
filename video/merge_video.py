from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(video_paths, output_path="merged_video.mp4"):
    """
    Merges a list of video files into a single video.

    :param video_paths: List of paths to video files.
    :param output_path: Path to save the merged video.
    """
    try:
        clips = [VideoFileClip(video) for video in video_paths]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_path, codec="libx264", fps=24)
        print(f"Merged video saved as: {output_path}")

        return output_path
    except Exception as e:
        print(f"Error: {e}")
    finally:
        for clip in clips:
            clip.close()
