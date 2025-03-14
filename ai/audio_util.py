# from typing import Sequence
# import os
# import json
# from dotenv import load_dotenv
# import google.cloud.texttospeech as tts
# from google.oauth2.service_account import Credentials
# from constants import audio_config
# import tempfile
# import logging

# # Load environment variables
# load_dotenv()

# # Get the API key from environment variables
# # Get the API key from environment variables
# # google_service_account = os.getenv('GOOGLE_SERVICE_ACCOUNT')
# google_service_account = os.getenv('GOOGLE_SERVICE_ACCOUNT')

# if google_service_account:
#     # Parse the JSON string into a dictionary
#     credentials_dict = json.loads(google_service_account)

#     # Write it to a temporary JSON file (Google APIs require a file path)
#     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#         json.dump(credentials_dict, temp_file)
#         temp_file_path = temp_file.name

#     # Set the environment variable for authentication
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path

# # if google_service_account:
# #     # Parse the JSON string into a dictionary
# #     credentials_dict = json.loads(google_service_account)

# #     # Write it to a temporary JSON file (Google APIs require a file path)
# #     with open("temp_gcp_credentials.json", "w") as temp_file:
# #         json.dump(credentials_dict, temp_file)

# #     # Set the environment variable for authentication
# #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "temp_gcp_credentials.json"

# # # Initialize the client
# # client = tts.TextToSpeechClient()


# class AudioUtil:
#     def __init__(self):
#         self.client = tts.TextToSpeechClient()
#         self.config = audio_config

#     def unique_languages_from_voices(self, voices: Sequence[tts.Voice]):
#         language_set = set()
#         for voice in voices:
#             for language_code in voice.language_codes:
#                 language_set.add(language_code)
#         return language_set

#     def list_languages(self):
#         response = self.client.list_voices()
#         languages = self.unique_languages_from_voices(response.voices)

#         print(f" Languages: {len(languages)} ".center(60, "-"))
#         for i, language in enumerate(sorted(languages)):
#             print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

#     def text_to_wav_from_config(self, input_text: str, output_filename: str = None):
#         """
#         Generates a WAV file from the given text using the provided configuration.

#         Args:
#             input_text: Text that is neede to converted into audio.
#             output_filename: The name of the output WAV file. If None, defaults to "{voice_name}.wav".

#         Returns:
#             The filename of the generated WAV file.
#             Raises an exception if there is an issue with the text to speech process.
#         """

#         try:
#             text_input = tts.SynthesisInput(text=input_text)
#             voice_params = tts.VoiceSelectionParams(
#                 language_code=self.config["voice"]["languageCode"], name=self.config["voice"]["name"]
#             )
#             audio_config = tts.AudioConfig(
#                 audio_encoding=getattr(tts.AudioEncoding, self.config["audioConfig"]["audioEncoding"]),  # Dynamic enum lookup
#                 effects_profile_id=self.config["audioConfig"].get("effectsProfileId"), # Handle optional effectsProfileId
#                 pitch=self.config["audioConfig"]["pitch"],
#                 speaking_rate=self.config["audioConfig"]["speakingRate"],
#             )

#             logging.info("Synthesizing speech.............")
#             response = self.client.synthesize_speech(
#                 input=text_input,
#                 voice=voice_params,
#                 audio_config=audio_config,
#             )
#             logging.info("Audio generated")

#             return response

#             # voice_name = self.config["voice"]["name"] # Extract voice name for default filename
#             # if output_filename is None:
#             #     filename = f"{voice_name}.wav"
#             # else:
#             #     filename = output_filename

#             # with open(filename, "wb") as out:
#             #     out.write(response.audio_content)
#             #     print(f'Generated speech saved to "{filename}"')
#             # return filename

#         except Exception as e:
#             print(f"Error during speech synthesis or file writing: {e}")
#             raise

# if __name__== "__main__":
#     audio_util = AudioUtil()
#     # audio_util.list_languages()
#     audio_util.text_to_wav_from_config("Hello, this is a test message", "test.wav")
#     os.remove("temp_gcp_credentials.json")  # Clean up the temporary credentials file

from typing import Sequence
import os
import json
import tempfile
import logging
from dotenv import load_dotenv
import google.cloud.texttospeech as tts
from constants import audio_config

# Load environment variables
load_dotenv()

google_service_account = os.getenv("GOOGLE_SERVICE_ACCOUNT")

google_service_account = google_service_account.replace("\n", "\\n")

google_service_account_dict = json.loads(google_service_account)
        
# Create a temporary file to store credentials
with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w") as temp_json:
    json.dump(google_service_account_dict, temp_json)
    temp_json_path = temp_json.name
    print(f"Temporary JSON file created: {temp_json_path}")
    
# Set the environment variable to point to this temp file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_json_path


class AudioUtil:
    def __init__(self):
        """Initializes the Google Cloud TTS client and handles credentials."""
        self.temp_file_path = None

        # Initialize the Text-to-Speech client
        self.client = tts.TextToSpeechClient()
        self.config = audio_config

    # def __del__(self):
    #     """Deletes temporary credentials file upon instance deletion."""
    #     if self.temp_file_path and os.path.exists(self.temp_file_path):
    #         os.remove(self.temp_file_path)
    #         logging.info("Temporary GCP credentials deleted.")

    def unique_languages_from_voices(self, voices: Sequence[tts.Voice]):
        language_set = {language_code for voice in voices for language_code in voice.language_codes}
        return language_set

    def list_languages(self):
        response = self.client.list_voices()
        languages = self.unique_languages_from_voices(response.voices)

        print(f" Languages: {len(languages)} ".center(60, "-"))
        for i, language in enumerate(sorted(languages)):
            print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

    def text_to_wav_from_config(self, input_text: str):
        """Generates speech from text using GCP TTS API."""
        try:
            text_input = tts.SynthesisInput(text=input_text)
            voice_params = tts.VoiceSelectionParams(
                language_code=self.config["voice"]["languageCode"],
                name=self.config["voice"]["name"],
            )
            audio_config = tts.AudioConfig(
                audio_encoding=getattr(tts.AudioEncoding, self.config["audioConfig"]["audioEncoding"]),
                effects_profile_id=self.config["audioConfig"].get("effectsProfileId"),
                pitch=self.config["audioConfig"]["pitch"],
                speaking_rate=self.config["audioConfig"]["speakingRate"],
            )

            logging.info("Synthesizing speech...")
            response = self.client.synthesize_speech(
                input=text_input,
                voice=voice_params,
                audio_config=audio_config,
            )
            logging.info("Audio generated successfully.")
            return response

        except Exception as e:
            logging.error(f"Error during speech synthesis: {e}")
            raise


if __name__ == "__main__":
    audio_util = AudioUtil()
    response = audio_util.text_to_wav_from_config("Hello, this is a test message")

    # Cleanup happens automatically when the object is deleted
