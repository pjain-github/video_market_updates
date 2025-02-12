from moviepy.video.fx.all import fadein, fadeout
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip
)
# from moviepy.video.VideoClip import ImageClip
import numpy as np

def generate_video(images, audios, intro_image, intro_audio, thank_you_image, thank_you_audio, output_path):
    # Load all audio clips
    audio_clips = [AudioFileClip(audio).set_fps(44100) for audio in audios]
    
    # Load intro and thank you audios
    intro_audio_clip = AudioFileClip(intro_audio).set_fps(44100)
    thank_you_audio_clip = AudioFileClip(thank_you_audio).set_fps(44100)

    # Load image clips
    image_clips = []

    # Add intro image (for intro audio)
    image_clips.append(ImageClip(intro_image).set_duration(intro_audio_clip.duration))

    # First image (for first audio)
    image_clips.append(ImageClip(images[0]).set_duration(audio_clips[0].duration))

    # Second and third images (for second audio)
    if len(images) > 2:
        half_duration = audio_clips[1].duration / 2
        image_clips.append(ImageClip(images[1]).set_duration(half_duration))
        image_clips.append(ImageClip(images[2]).set_duration(half_duration))
    else:
        image_clips.append(ImageClip(images[1]).set_duration(audio_clips[1].duration))

    # Fourth image (for third audio)
    if len(images) > 3:
        image_clips.append(ImageClip(images[3]).set_duration(audio_clips[2].duration))

    # Add thank you image (for thank you audio)
    image_clips.append(ImageClip(thank_you_image).set_duration(thank_you_audio_clip.duration))

    # Apply fade transitions between clips
    for i in range(len(image_clips) - 1):
        image_clips[i] = fadeout(image_clips[i], 1)
        image_clips[i + 1] = fadein(image_clips[i + 1], 1)

    # Create silence (1.5s) between audio clips
    silence = AudioFileClip(audios[0]).set_duration(1.5).volumex(0)

    # Concatenate audio clips with silence
    final_audio = concatenate_audioclips([
        intro_audio_clip, silence,  # Intro
        audio_clips[0], silence,  # First segment
        audio_clips[1], silence,  # Second segment
        audio_clips[2], silence,  # Third segment
        thank_you_audio_clip  # Thank You
    ])

    # Concatenate image clips into a video
    video = concatenate_videoclips(image_clips, method="compose")

    # Attach final audio to the video
    final_video = video.set_audio(final_audio)

    # Write the final video file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)