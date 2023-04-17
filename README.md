# Video Subtitler

## Overview

Video subtitling is an important part of video production that enables viewers who are hearing-impaired or who speak different languages to enjoy and understand video content. With the growth of online video platforms and global communication, the demand for multilingual subtitling has increased significantly. The video-subtitler project on GitHub provides a solution for adding subtitles to videos in multiple languages.

The video-subtitler project is an open-source Python project that leverages popular libraries such as ffmpeg and openAI whisper. These libraries provide powerful functionality for handling various video formats and recognizing text in different languages.

## Installation

To use the video-subtitler project, you will need to have Python 3 installed on your system. You can download and install Python 3 from the official Python website: https://www.python.org/downloads/

After installing Python, you can install the required libraries using pip. The following command will install the necessary libraries:

```
$ pip install requirements.txt
```


Once you have installed the necessary libraries, you can download the video-subtitler project from GitHub by cloning the repository:

```
$ git clone https://github.com/KarinBrisker/video-subtitler.git
```


## Usage

The video-subtitler project provides a command-line interface for adding subtitles to videos in multiple languages. To use the project, you will need to have a video file and a text file containing the subtitles in the target languages. The following command will add subtitles to a video:

```
python video_subtitler.py --video /path/to/video.mp4 --subtitles /path/to/subtitles.txt --languages en fr es
```


In this command, the `--video` flag specifies the path to the input video file, the `--subtitles` flag specifies the path to the subtitles text file, and the `--languages` flag specifies the target languages for the subtitles.

The video-subtitler project supports several output subtitle file formats, including SRT and VTT.

## Demo
- todo

## Conclusion

The video-subtitler project on GitHub is a powerful and easy-to-use tool for adding subtitles to videos in multiple languages. With its simple command-line interface and robust functionality, the project is ideal for beginners and experts alike. Whether you are producing videos for a global audience or simply want to make your content more accessible, the video-subtitler project can help you achieve your goals.

## License
