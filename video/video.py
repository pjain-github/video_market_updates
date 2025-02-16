import os
import tempfile
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
import logging


# def create_video_with_audio(tts_response, image, output_video_path=None):
#     # Create a temporary audio file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
#         temp_audio.write(tts_response.audio_content)
#         temp_audio_path = temp_audio.name  # Store the path

#     try:
#         # Load audio file with MoviePy
#         audio_clip = AudioFileClip(temp_audio_path)
#         audio_duration = audio_clip.duration  # Get audio length in seconds

#         # Convert PIL Image to Full HD (1920x1080) and save as temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
#             image = image.resize((1920, 1080))
#             image.save(temp_image.name)
#             temp_image_path = temp_image.name  # Store the path

#         # Create a video clip from the image, setting duration to match audio
#         video_clip = ImageClip(temp_image_path, duration=audio_duration)
#         video_clip = video_clip.set_audio(audio_clip).set_fps(30)

#         logging.info("Video generated successfully")

#         # Export final video (uncomment if you want to save it)
#         # video_clip.write_videofile("sample1.mp4", codec="libx264", audio_codec="aac", fps=30)

#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#         temp_path = temp_file.name
#         temp_file.close()  # Close so moviepy can write to it
#         video_clip.write_videofile(temp_path, codec="libx264", audio_codec="aac", fps=30)

#         return temp_path

#     finally:
#         # Ensure cleanup
#         if 'audio_clip' in locals():
#             audio_clip.close()  # Explicitly close the audio clip before deleting the file

#         os.remove(temp_audio_path)
#         os.remove(temp_image_path)


# def create_video_with_audio_saved(audio_path, image, output_video_path=None):

#     temp_audio_path = audio_path

#     try:
#         # Load audio file with MoviePy
#         audio_clip = AudioFileClip(temp_audio_path)
#         audio_duration = audio_clip.duration  # Get audio length in seconds

#         # Convert PIL Image to Full HD (1920x1080) and save as temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
#             image = image.resize((1920, 1080))
#             image.save(temp_image.name)
#             temp_image_path = temp_image.name  # Store the path

#         # Create a video clip from the image, setting duration to match audio
#         video_clip = ImageClip(temp_image_path, duration=audio_duration)
#         video_clip = video_clip.set_audio(audio_clip).set_fps(30)

#         logging.info("Video generated successfully")

#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#         temp_path = temp_file.name
#         temp_file.close()  # Close so moviepy can write to it
#         video_clip.write_videofile(temp_path, codec="libx264", audio_codec="aac", fps=30)

#         # Export final video (uncomment if you want to save it)
#         # video_clip.write_videofile("sample1.mp4", codec="libx264", audio_codec="aac", fps=30)

#         return temp_path

#     finally:
#         # Ensure cleanup
#         if 'audio_clip' in locals():
#             audio_clip.close()  # Explicitly close the audio clip before deleting the file

#         os.remove(temp_image_path)

def create_video_with_audio(tts_response, image, output_video_path=None):
    # Create a temporary audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(tts_response.audio_content)
        temp_audio_path = temp_audio.name  # Store the path

    try:
        # Load audio file with MoviePy
        audio_clip = AudioFileClip(temp_audio_path)
        audio_duration = audio_clip.duration  # Get audio length in seconds

        # Convert PIL Image to Full HD (1920x1080) and save as temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
            image = image.resize((1920, 1080))
            image.save(temp_image.name)
            temp_image_path = temp_image.name  # Store the path

        # Create a video clip from the image, setting duration to match audio + fade-in/out duration
        total_duration = audio_duration + 1.4  # Adding 0.7s fade-in and 0.7s fade-out

        video_clip = ImageClip(temp_image_path, duration=total_duration).set_fps(30)

        # Apply fade-in (0.7s) and fade-out (0.7s)
        video_clip = video_clip.fadein(0.7).fadeout(0.7)

        # Shift audio to start after 0.7 seconds
        audio_clip = audio_clip.set_start(0.7)

        # Combine video and audio
        final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip)])

        logging.info("Video generated successfully")

        # Export final video
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_path = temp_file.name
        temp_file.close()  # Close so moviepy can write to it
        final_clip.write_videofile(temp_path, codec="libx264", audio_codec="aac", fps=30)

        return temp_path

    finally:
        # Ensure cleanup
        if 'audio_clip' in locals():
            audio_clip.close()  # Explicitly close the audio clip before deleting the file

        os.remove(temp_audio_path)
        os.remove(temp_image_path)


def create_video_with_audio_saved(audio_path, image, output_video_path=None):

    temp_audio_path = audio_path

    try:
        # Load audio file with MoviePy
        audio_clip = AudioFileClip(temp_audio_path)
        audio_duration = audio_clip.duration  # Get audio length in seconds

        # Convert PIL Image to Full HD (1920x1080) and save as temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image:
            image = image.resize((1920, 1080))
            image.save(temp_image.name)
            temp_image_path = temp_image.name  # Store the path

        # Create a video clip from the image, setting duration to match audio + fade-in/out duration
        total_duration = audio_duration + 1.4  # Adding 0.7s fade-in and 0.7s fade-out

        video_clip = ImageClip(temp_image_path, duration=total_duration).set_fps(30)

        # Apply fade-in (0.7s) and fade-out (0.7s)
        video_clip = video_clip.fadein(0.7).fadeout(0.7)

        # Shift audio to start after 0.7 seconds
        audio_clip = audio_clip.set_start(0.7)

        # Combine video and audio
        final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip)])

        logging.info("Video generated successfully")

        # Export final video
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_path = temp_file.name
        temp_file.close()  # Close so moviepy can write to it
        final_clip.write_videofile(temp_path, codec="libx264", audio_codec="aac", fps=30)

        return temp_path

    finally:
        # Ensure cleanup
        if 'audio_clip' in locals():
            audio_clip.close()  # Explicitly close the audio clip before deleting the file

        os.remove(temp_image_path)
