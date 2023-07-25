from flask import Flask, request, jsonify, render_template, escape
import os
import soundfile as sf
import numpy as np
import json
from pydub import AudioSegment
import datetime
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from helpers import embed_watermark

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.secret_key = 'your_secret_key'

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Implement a function to load and return a user object based on the user_id
    return User.get(user_id)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        # Implement a function to retrieve a user object by ID
        # ...
        return User(user_id, 'username', 'password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Implement login logic, validate user credentials, and login the user
        user = User.get(1)  # Fetch user object based on username
        if user and user.password == password:
            login_user(user)  # user is the authenticated user object
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'})
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Redirect to the appropriate page after logout
    return jsonify({'success': True})

@app.route('/protected_resource')
@login_required
def protected_resource():
    # Only authenticated users can access this endpoint
    return jsonify({'message': 'Access granted'})

def extract_watermark(audio_file):
    # Load the audio file
    audio, _ = sf.read(audio_file)

    # Perform watermark extraction logic
    # Replace this with your actual watermark extraction algorithm

    watermark = "Sample Watermark"  # Placeholder for the extracted watermark
    return watermark

def authenticate_watermark(watermark, existing_data):
    # Perform watermark authentication logic
    # Replace this with your actual watermark authentication algorithm

    is_authentic = True  # Placeholder for the authentication result
    return is_authentic

@app.route('/analyze', methods=['POST', 'GET'])
def analyze_endpoint():
    if request.method == 'POST':
        audio_file = request.files.get('audio_file')
        existing_data = request.form.get('existing_data')

        # Check the file extension
        file_extension = os.path.splitext(audio_file.filename)[1]
        if file_extension.lower() in ['.wav', '.mp3']:
            # Perform watermark analysis
            watermark = extract_watermark(audio_file)
            is_authentic = authenticate_watermark(watermark, existing_data)

            # Return the result
            return jsonify({'watermark': watermark, 'is_authentic': is_authentic})
        else:
            return jsonify({'error': 'Invalid file format. Only .wav and .mp3 files are supported.'}), 400
    else:
        # Render the analyze.html template
        return render_template('analyze.html')

@app.route('/embed', methods=['POST', 'GET'])
@login_required
def embed_endpoint():
    if request.method == 'POST':
        audio_file = request.files.get('audio_file')
        artist_name = escape(request.form.get('artist_name'))
        track_name = escape(request.form.get('track_name'))

        # Create a dictionary with the parameters
        watermark_data = {
            'artist_name': artist_name,
            'track_name': track_name
        }

        # Convert the dictionary to a JSON string
        watermark_message = json.dumps(watermark_data)

        # Check the file extension
        file_extension = os.path.splitext(audio_file.filename)[1]
        if file_extension.lower() in ['.wav', '.mp3']:
            # Save the audio file temporarily
            audio_file_path = 'music_files/temp/original' + file_extension
            audio_file.save(audio_file_path)

            # Convert all files to WAV format for watermarking
            if file_extension.lower() == '.mp3':
                wav_file_path = 'music_files/temp/original.wav'
                mp3_to_wav(audio_file_path, wav_file_path)
                os.remove(audio_file_path)  # Remove the original audio file
            else:
                wav_file_path = audio_file_path

            # Call the watermark embedding function using the provided audio file and watermark message
            watermarked_file = embed_watermark(wav_file_path, watermark_message)

            # Generate a timestamp-based filename for the watermarked file
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            watermarked_file_path = f'music_files/original/stronger_{timestamp}' + file_extension
            os.rename(watermarked_file, watermarked_file_path)

            # Return the filename of the watermarked audio file
            return jsonify({'watermarked_audio': watermarked_file_path})
        else:
            return jsonify({'error': 'Invalid file format. Only .wav and .mp3 files are supported.'}), 400
    else:
        # Render the embed.html template
        return render_template('embed.html')

@app.route('/compare', methods=['POST', 'GET'])
@login_required
def compare_endpoint():
    if request.method == 'POST':
        original_file = request.files.get('original_file')
        watermarked_file = request.files.get('watermarked_file')

        # Save the original and watermarked files temporarily
        original_file_path = 'music_files/original/Stronger.wav'
        watermarked_file_path = 'music_files/watermarked/watermarked_file.wav'
        original_file.save(original_file_path)
        watermarked_file.save(watermarked_file_path)

        # Call the comparison function
        result = compare_audio(original_file_path, watermarked_file_path)

        # Remove the temporary files
        os.remove(original_file_path)
        os.remove(watermarked_file_path)

        # Return the result
        return jsonify({'result': result})
    else:
        # Render the compare.html template
        return render_template('compare.html')

def compare_audio(original_file, watermarked_file):
    # Load the original audio
    original_audio, _ = sf.read(original_file)

    # Load the watermarked audio
    watermarked_audio, _ = sf.read(watermarked_file)

    #Check if the audio lengths are the same
    if len(original_audio) != len(watermarked_audio):
        return "Audio files have different lengths"

    # Calculate the difference between the original and watermarked audio
    diff = np.abs(original_audio - watermarked_audio)

    # Compute the mean difference
    mean_diff = np.mean(diff)

    # Return the result
    if mean_diff < 1e-6:
        return "Audio is likely watermarked"
    else:
        return "Audio is not watermarked"

def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format='wav')

if __name__ == '__main__':
    app.run()
