import os
from typing import Dict

import torch
import whisper

import numpy as np  # for counting parameters

from utils import log

device = "cuda" if torch.cuda.is_available() else "cpu"


class TranscribeAudio:
    def __init__(self):
        self.model = whisper.load_model("base", device=device)
        log(
            f"Model is {'multilingual' if self.model.is_multilingual else 'English-only'} "
            f"and has {sum(np.prod(p.shape) for p in self.model.parameters()):,} parameters."
        )

    def transcribe(self, audio_file_path: str, language: str = "en") -> Dict:
        log(f"Transcribing {audio_file_path} in {language}")
        options = dict(language=language, beam_size=5, best_of=5)
        transcribe_options = dict(task="transcribe", **options)
        result = self.model.transcribe(audio_file_path, **transcribe_options)
        return result

    def save_output(self, transcript_output: Dict, audio_file_path: str) -> str:
        filename, ext = os.path.splitext(audio_file_path)
        directory = os.path.dirname(filename)
        log(f"Saving output to {directory} directory as {filename}.vtt")
        srt_writer = whisper.utils.get_writer("srt", directory)
        vtt_writer = whisper.utils.get_writer("vtt", directory)

        # Save as an SRT file
        srt_writer(result=transcript_output, audio_path=audio_file_path)

        # Save as a VTT file
        vtt_writer(result=transcript_output, audio_path=audio_file_path)

        return f"{filename}.vtt"

    def __call__(self, audio_file_path: str, output_dir: str, input_language: str = "en") -> str:
        transcript = self.transcribe(audio_file_path)
        transcript_path = self.save_output(transcript, audio_file_path)
        return transcript_path


if __name__ == '__main__':
    transcribe_audio = TranscribeAudio()
    transcribe_audio('sample', 'iPhone_14_Pro.mp3')
