import gradio as gr
import os
import json

with open('resources/languages.json', 'r') as f:
    code2lang = json.load(f)

# language code lookup by name, with a few language aliases
lang2code = {
    **{language: code for code, language in code2lang.items()},
}

LANGS = sorted(lang2code.keys())


def video_identity(video, lang1="en", lang2="en"):
    return video


demo = gr.Interface(video_identity,
                    inputs=[gr.Video(),
                            gr.components.Dropdown(label="Source Language", choices=LANGS, default="english"),
                            gr.components.Dropdown(label="Target Language", choices=LANGS, default="english"),
                            ],
                    outputs="playable_video",
                    examples=[[
                        os.path.join(os.path.dirname(__file__),
                                     "sample/iPhone_14_Pro.mp4"), "en"]],
                    cache_examples=True,
                    title="Video Subtitler Demo",
                    description="This demo is a proof of concept for a video subtitler. "
                    )

if __name__ == "__main__":
    demo.launch()
