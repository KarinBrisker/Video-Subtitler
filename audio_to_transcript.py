import whisper
from whisper.utils import get_writer

import numpy as np  # for counting parameters


class TranscribeAudio:
    def __init__(self):
        self.model = whisper.load_model("base")
        print(
            f"Model is {'multilingual' if self.model.is_multilingual else 'English-only'} "
            f"and has {sum(np.prod(p.shape) for p in self.model.parameters()):,} parameters."
        )
        self.options = {"max_line_width": 20, "max_line_count": 3, "highlight_words": True}

    def transcribe(self, audio_file_path, language="en"):
        result = self.model.transcribe(audio_file_path, language=language)
        return result

    def save_output(self, output_path, transcript_output, audio):
        # Save as an SRT file
        srt_writer = get_writer("srt", output_path)
        srt_writer(transcript_output, audio, self.options)

        # Save as a VTT file
        vtt_writer = get_writer("vtt", output_path)
        vtt_writer(transcript_output, audio, self.options)


if __name__ == '__main__':
    transcribe_audio = TranscribeAudio()
    transcript = transcribe_audio.transcribe('sample/iPhone_14_Pro.mp3')
    transcribe_audio.save_output('sample', transcript, 'sample/iPhone_14_Pro.mp3')
