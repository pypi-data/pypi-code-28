from __future__ import print_function
import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback

speech_to_text = SpeechToTextV1(
    username='YOUR SERVICE USERNAME',
    password='YOUR SERVICE PASSWORD',
    url='https://stream.watsonplatform.net/speech-to-text/api')

## If service instance provides API key authentication
# speech_to_text = SpeechToTextV1(
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
#     url='https://stream.watsonplatform.net/speech-to-text/api',
#     iam_api_key='your_api_key')

print(json.dumps(speech_to_text.list_models(), indent=2))

print(json.dumps(speech_to_text.get_model('en-US_BroadbandModel'), indent=2))

with open(join(dirname(__file__), '../resources/speech.wav'),
          'rb') as audio_file:
    print(
        json.dumps(
            speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                timestamps=True,
                word_confidence=True),
            indent=2))

# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Transcription completed')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

mycallback = MyRecognizeCallback()
with open(join(dirname(__file__), '../resources/speech.wav'),
          'rb') as audio_file:
    speech_to_text.recognize_using_websocket(audio=audio_file, content_type="audio/l16; rate=44100",
                                             recognize_callback=mycallback)
