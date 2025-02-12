from ai.audio_util import AudioUtil

def generate_intro_audio(text: str):

    audio_util = AudioUtil()

    audio_util.text_to_wav_from_config(text, "elements/intro_audio.wav")

def generate_outro_audio(text: str):

    audio_util = AudioUtil()

    audio_util.text_to_wav_from_config(text, "elements/outro_audio.wav")

if __name__=="__main__":

    generate_intro_audio("Hi, welcome to Fin Insights AI. Here's your daily Indian stock market update, powered by AI.")
    generate_outro_audio("Thank you for watching! Subscribe to never miss any updates from us.")