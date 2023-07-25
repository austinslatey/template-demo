# LoopPRINT

# Watermarking Functionality
The "Watermarking Audio" application allows you to embed and extract watermarks in audio files. It provides a web server built using Flask, where you can send HTTP POST requests to interact with the application.


## Prerequisites
Before using the application, make sure you have the following installed:

- Python 3.x
- Flask
- librosa
- numpy
- soundfile

## File Structure
app.py
helpers.py
music_files/
    original/
        test.mp3
    watermarked/
        watermarked_audio.wav
temp/


## Usage
Run the Flask server by executing the command `python app.py`. The server will start running on http://localhost:5000.

Send HTTP POST requests to the following endpoints using a tool like cURL, Postman, or a custom script:

/analyze: Analyzes an audio file and extracts the watermark.

Method: POST
Endpoint: http://localhost:5000/analyze
Form Data:
audio_file: Select the audio file from the music_files folder.
existing_data: Provide any existing data that may be embedded in the audio file.
Response: Returns the extracted watermark and authentication status.
/embed: Embeds a watermark in an audio file.

Method: POST
Endpoint: http://localhost:5000/embed
Form Data:
audio_file: Select the audio file from the music_files folder.
watermark_message: Provide the watermark message you want to embed in the audio file.
Response: Returns the filename of the watermarked audio file.
/compare: Compares an original audio file with a watermarked audio file.

Method: POST
Endpoint: http://localhost:5000/compare
Form Data:
original_file: Select the original audio file from the music_files folder.
watermarked_file: Select the watermarked audio file from the music_files folder.
Response: Returns the result of the comparison, indicating whether the audio is likely watermarked or not.
You can integrate the above HTTP POST requests into your own script or application by using the requests library.

Handle the responses returned by the server appropriately in your script or application. For example, you can store the values of the extracted watermark and authentication status, or the result of the comparison, in variables for further processing or analysis.



