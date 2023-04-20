import gradio as gr
import os
from main import LANGS, Pipeline


def video_identity(video, source_language="English", target_language="Spanish"):
    pipeline = Pipeline()
    video_path = pipeline(video, "sample", source_language, target_language)

    return video_path


demo = gr.Interface(video_identity,
                    inputs=[gr.Video(),
                            gr.components.Dropdown(label="Source Language", choices=LANGS),
                            gr.components.Dropdown(label="Target Language", choices=LANGS),
                            ],
                    outputs="playable_video",
                    examples=[[
                        os.path.join(os.path.dirname(__file__),
                                     "sample/iPhone_14_Pro.mp4"), "English"]],
                    cache_examples=True,
                    title="Video Subtitler Demo 🍿🍿🍿",
                    description="This demo is a proof of concept for a video subtitler. "
                    )

pipeline = Pipeline()
demo.queue(max_size=15).launch(show_error=True)