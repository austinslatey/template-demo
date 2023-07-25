import unittest
from helpers import embed_watermark, extract_watermark

class WatermarkingTests(unittest.TestCase):
    def test_embed_watermark(self):
        audio_file = "./music_files/test.mp3"
        watermark_message = "Sample Watermark Message"
        watermarked_audio = embed_watermark(audio_file, watermark_message)
        # Assert that the watermarked_audio is not empty or None
        self.assertIsNotNone(watermarked_audio)
        self.assertNotEqual(len(watermarked_audio), 0)

    def test_extract_watermark(self):
        audio_file = "./music_files/test.mp3"
        existing_data = "Sample Existing Data"
        watermark, is_authentic = extract_watermark(audio_file, existing_data)
        # Assert that the extracted watermark is not empty or None
        self.assertIsNotNone(watermark)
        self.assertNotEqual(len(watermark), 0)
        # Assert that the is_authentic is True
        self.assertTrue(is_authentic)

if __name__ == '__main__':
    unittest.main()
