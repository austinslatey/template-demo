import numpy as np
import librosa
from soundfile import write as write_wav


def embed_watermark(audio_file, watermark_message):
    # Load the audio file
    audio, sr = librosa.load(audio_file)

    # Convert the watermark message to binary
    binary_watermark = ''.join(format(ord(c), '08b') for c in watermark_message)

    # Create a copy of the audio signal for modification
    watermarked_audio = audio.copy()

    # Embed the watermark in the audio signal
    watermark_length = len(binary_watermark)

    for i in range(watermark_length):
        if i < len(watermarked_audio):
            sample = watermarked_audio[i]
            binary_sample = format(int(sample * 32767), '016b')
            modified_sample = binary_sample[:-1] + binary_watermark[i]
            watermarked_audio[i] = int(modified_sample, 2) / 32767

    # Save the modified audio to a new file
    watermarked_file = "watermarked_audio.wav"
    write_wav(watermarked_file, watermarked_audio, sr)

    return watermarked_file

def extract_watermark(audio_file, existing_data):
    # Load the audio file
    audio, sr = librosa.load(audio_file)

    # Extract the watermark from the audio signal
    watermark_length = len(existing_data)
    extracted_watermark = ''

    for i in range(watermark_length):
        if i < len(audio):
            sample = audio[i]
            binary_sample = format(int(sample * 32767), '016b')
            extracted_bit = binary_sample[-1]
            extracted_watermark += extracted_bit

    # Convert the extracted binary watermark to text
    watermark_message = ''.join(chr(int(
        extracted_watermark[i:i+8], 2)) for i in range(0, len(extracted_watermark), 8))

    return watermark_message, True
