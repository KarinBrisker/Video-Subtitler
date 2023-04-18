import os

from googletrans import Translator

from gradio_app import code2lang
from utils import log


class MyTranslator:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text_file_path, source_language, target_language):
        # Open the input file and read its contents
        with open(text_file_path, 'r') as f:
            input_text = f.read()

        filename, ext = os.path.splitext(text_file_path)
        output_file_path = f"{filename}_translated{ext}"
        log(f"Translating text to {code2lang[target_language]} and saving to {output_file_path}")
        # Translate the text to the desired language
        output_text = self.translator.translate(input_text, dest=target_language).text
        # Write the translated text to the output file
        with open(output_file_path, 'w') as f:
            f.write(output_text)

        return output_file_path


if __name__ == '__main__':
    translator = MyTranslator()
    translation_path = translator.translate('sample/iPhone_14_Pro.vtt', 'en', 'es')
