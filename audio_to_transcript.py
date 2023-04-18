import os
from typing import Dict

import whisper
from whisper.utils import get_writer

import numpy as np  # for counting parameters

from gradio_app import code2lang
from utils import log


class TranscribeAudio:
    def __init__(self):
        self.model = whisper.load_model("base")
        log(
            f"Model is {'multilingual' if self.model.is_multilingual else 'English-only'} "
            f"and has {sum(np.prod(p.shape) for p in self.model.parameters()):,} parameters."
        )
        self.options = {"max_line_width": 20, "max_line_count": 3, "highlight_words": True}

    def transcribe(self, audio_file_path: str, language: str = "en") -> Dict:
        log(f"Transcribing {audio_file_path} in {code2lang[language]}")
        options = dict(language=language, beam_size=5, best_of=5)
        transcribe_options = dict(task="transcribe", **options)
        result = self.model.transcribe(audio_file_path, **transcribe_options)
        return result

    def translate(self, audio_file_path, language="en"):
        log(f"Translating {audio_file_path} to {code2lang[language]}")
        options = dict(language=language, beam_size=5, best_of=5)
        translate_options = dict(task="translate", **options)
        result = self.model.transcribe(audio_file_path, **translate_options)
        return result

    def save_output(self, transcript_output: Dict, audio_file_path: str) -> str:
        filename, ext = os.path.splitext(audio_file_path)
        directory = os.path.dirname(filename)
        log(f"Saving output to {directory} directory as {filename}.vtt")
        # Save as an SRT file
        srt_writer = get_writer("srt", directory)
        srt_writer(transcript_output, audio_file_path, self.options)

        # Save as a VTT file
        vtt_writer = get_writer("vtt", directory)
        vtt_writer(transcript_output, audio_file_path, self.options)

        return f"{filename}.vtt"

    def __call__(self, audio_file_path: str, output_dir: str, input_language: str = "en", output_language: str = "en") -> str:
        transcript = self.transcribe(audio_file_path, input_language)
        if input_language != output_language:
            translated_transcript = self.translate(audio_file_path, output_language)
            transcript_path = self.save_output(translated_transcript, audio_file_path)
        else:
            transcript_path = self.save_output(transcript, audio_file_path)
        return transcript_path


if __name__ == '__main__':
    transcribe_audio = TranscribeAudio()
    transcribe_audio('sample', 'iPhone_14_Pro.mp3')
