import os
import subprocess

import ffmpeg

from utils import log


class VideoToAudioConverter:
    @staticmethod
    def convert(path_to_video: str, output_ext="mp3") -> str:
        """Converts video to audio directly using `ffmpeg` command
        with the help of subprocess module"""
        log("Converts video to audio")
        filename, ext = os.path.splitext(path_to_video)
        subprocess.call(["ffmpeg",
                         "-y",
                         "-i",
                         path_to_video,
                         f"{filename}.{output_ext}"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

        video_length = float(ffmpeg.probe(path_to_video)['format']['duration'])
        audio_length = float(ffmpeg.probe(f"{filename}.{output_ext}")['format']['duration'])
        if video_length - audio_length > 1:
            raise Exception("Conversion failed")
        return f"{filename}.{output_ext}"


if __name__ == '__main__':
    video_to_audio_converter = VideoToAudioConverter()
    video_to_audio_converter.convert('iPhone_14_Pro.mp4')
    if os.path.exists('sample/iPhone_14_Pro.mp3'):
        log("File converted successfully")
    else:
        log("File conversion failed")
