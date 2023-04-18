import subprocess

from audio_to_transcript import TranscribeAudio
from translator import MyTranslator
from utils import log
from video_to_audio_converter import VideoToAudioConverter


class Pipeline:
    def __init__(self):
        self.video_to_audio = VideoToAudioConverter()
        self.audio_to_text = TranscribeAudio()
        self.translator = MyTranslator()

    def __call__(self, video_path: str, output_path: str, input_language: str, output_language: str):
        audio_path = self.video_to_audio.convert(video_path)
        subtitle_path = self.audio_to_text(audio_path, output_path, input_language)
        if input_language != output_language:
            subtitle_path = self.translator.translate(subtitle_path, input_language, output_language)
        log(f"Embedding subtitles on input video and saves output video to {output_path}/output.mp4")
        # Use ffmpeg to add the subtitles to the input MP4 file and create the output MP4 file
        subtitles_cmd = ["ffmpeg", "-i", video_path, "-vf", f"subtitles={subtitle_path}", "-c:a", "copy",
                         f"{output_path}/output.mp4"]
        subprocess.run(subtitles_cmd, check=True)


if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline("sample/iPhone_14_Pro.mp4", "sample", "en", "es")
