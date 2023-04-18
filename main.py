import argparse
import json
import os
import subprocess

from audio_to_transcript import TranscribeAudio
from translator import MyTranslator
from utils import log
from video_to_audio_converter import VideoToAudioConverter

with open('resources/languages.json', 'r') as f:
    code2lang = json.load(f)

# language code lookup by name, with a few language aliases
lang2code = {
    **{language: code for code, language in code2lang.items()},
}

LANGS = sorted(lang2code.keys())


class Pipeline:
    def __init__(self):
        self.video_to_audio = VideoToAudioConverter()
        self.audio_to_text = TranscribeAudio()
        self.translator = MyTranslator()

    def __call__(self, video_path: str, output_path: str, input_language: str, output_language: str):
        filename, ext = os.path.splitext(video_path)

        audio_path = self.video_to_audio.convert(video_path)
        subtitle_path = self.audio_to_text(audio_path, output_path, input_language)
        if input_language != output_language:
            subtitle_path = self.translator.translate(subtitle_path, lang2code[input_language],
                                                      lang2code[output_language])
        log(f"Embedding subtitles on input video and saves output video to {output_path}/output.mp4")
        # Use ffmpeg to add the subtitles to the input MP4 file and create the output MP4 file

        subtitles_cmd = ["ffmpeg", "-y", "-i", video_path, "-vf", f"subtitles={subtitle_path}", "-c:a", "copy",
                         f"{filename}_{output_language}_output.mp4"]

        subprocess.run(subtitles_cmd, check=True)
        return f"{filename}_{output_language}_output.mp4"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", type=str,
                        help="video path to transcribe")
    parser.add_argument("--output_dir", "-o", type=str,
                        default=".", help="directory to save the outputs")
    parser.add_argument("--input_language", type=str, default=None, choices=LANGS,
                        help="language spoken in the video, skip to perform language detection")
    parser.add_argument("--output_language", type=str, default=None, choices=LANGS,
                        help="required translation language")

    args = parser.parse_args()
    pipeline = Pipeline()
    pipeline(args.video, args.output_dir, args.input_language, args.output_language)
