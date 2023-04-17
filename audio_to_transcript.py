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

    def transcribe(self, audio_file_path, language="en"):
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

    def save_output(self, output_path, transcript_output, audio):
        log(f"Saving output to {output_path} directory")
        # Save as an SRT file
        srt_writer = get_writer("srt", output_path)
        srt_writer(transcript_output, audio, self.options)

        # Save as a VTT file
        vtt_writer = get_writer("vtt", output_path)
        vtt_writer(transcript_output, audio, self.options)


if __name__ == '__main__':
    transcribe_audio = TranscribeAudio()
    transcript = transcribe_audio.transcribe('sample/iPhone_14_Pro.mp3')
    translated_transcript = transcribe_audio.translate('sample/iPhone_14_Pro.mp3', language="he")
    transcribe_audio.save_output('sample', translated_transcript, 'sample/iPhone_14_Pro.mp3')
