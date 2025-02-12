# import moviepy.video.fx.FadeIn as fadein
# import moviepy.video.fx.FadeOut as fadeout
# from moviepy.video.VideoClip import ImageClip
# from moviepy.audio.io.AudioFileClip import AudioFileClip
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


def generate_video(images, audios, output_path):
    # Load audio clips
    audio_clips = [AudioFileClip(audio).set_fps(44100) for audio in audios]

    # Load image clips
    image_clips = []

    # First image (for first audio)
    image_clips.append(
        ImageClip(images[0]).set_duration(audio_clips[0].duration)
    )

    # Second and third images (for second audio)
    if len(images) > 2:
        half_duration = audio_clips[1].duration / 2
        image_clips.append(
            ImageClip(images[1]).set_duration(half_duration)
        )
        image_clips.append(
            ImageClip(images[2]).set_duration(half_duration)
        )
    else:
        image_clips.append(
            ImageClip(images[1]).set_duration(audio_clips[1].duration)
        )

    # Fourth image (for third audio)
    if len(images) > 3:
        image_clips.append(
            ImageClip(images[3]).set_duration(audio_clips[2].duration)
        )

    # Apply fade transitions
    for i in range(len(image_clips) - 1):
        image_clips[i] = fadeout(image_clips[i], 1)
        image_clips[i + 1] = fadein(image_clips[i + 1], 1)

    # Add 1.5s silence between audio clips
    silence = AudioFileClip(audios[0]).set_duration(1.5).volumex(0)
    final_audio = concatenate_audioclips(
        [audio_clips[0], silence, audio_clips[1], silence, audio_clips[2]]
    )

    # Concatenate image clips into a video
    video = concatenate_videoclips(image_clips, method="compose")

    # Attach final audio to the video
    final_video = video.set_audio(final_audio)

    # Write the final video file
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)


# Example usage
if __name__=="__main__":
    pass
