import os
import subprocess

import ffmpeg


class VideoToAudioConverter:
    @staticmethod
    def convert(path_to_video, output_ext="mp3"):
        """Converts video to audio directly using `ffmpeg` command
        with the help of subprocess module"""
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
        print(video_length, audio_length)
        if video_length - audio_length > 1:
            raise Exception("Conversion failed")


if __name__ == '__main__':
    video_to_audio_converter = VideoToAudioConverter()
    video_to_audio_converter.convert('sample/iPhone_14_Pro.mp4')
    if os.path.exists('sample/iPhone_14_Pro.mp3'):
        print("File converted successfully")
    else:
        print("File conversion failed")
