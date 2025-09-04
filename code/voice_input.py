import gradio as gr
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
import io


# 其他代码保持不变

def another_function():

    with gr.Blocks() as another_demo:
        gr.Markdown("### Chat Interface with Voice Input")

        # 聊天界面
        # chatbot = gr.Chatbot()
        # with gr.Row():
        #     with gr.Column(scale=4):
        #         with gr.Column(scale=50):
        #             user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10, container=False)
        #         with gr.Column(min_width=32, scale=1):
        #             submitBtn = gr.Button("Submit", variant="primary")
        #     with gr.Column(scale=1):
        #         emptyBtn = gr.Button("Clear History")

        # 添加语音输入组件
        audio_input = gr.Audio(type="numpy")
        audio_button = gr.Button("Transcribe Audio")
        audio_output = gr.Textbox(label="Transcription")

        audio_button.click(transcribe_audio, inputs=audio_input, outputs=audio_output)

    return another_demo


def transcribe_audio(audio):
    # 创建一个识别器实例
    recognizer = sr.Recognizer()

    try:
        # 确保 audio 是一个包含 NumPy 数组的列表
        if not isinstance(audio, list) and isinstance(audio, tuple) and len(audio) == 2:
            audio_data = audio[1]  # 提取音频数据
        elif isinstance(audio, list) and isinstance(audio[0], np.ndarray):
            audio_data = audio[0]  # 直接使用音频数据
        else:
            return "Invalid audio input: Expected a tuple or a list containing a NumPy array."

        # 打印音频数据的形状以进行调试
        print(f"Audio data shape: {audio_data.shape}")

        # 确保音频数据是合适的格式
        if audio_data.ndim > 1:
            audio_data = audio_data.flatten()

        if audio_data.ndim != 1:
            raise ValueError("Audio data must be a 1D array")

        # 创建 AudioSegment
        audio_segment = AudioSegment(
            audio_data.tobytes(),  # 将 NumPy 数组转换为字节
            frame_rate=44100,
            sample_width=2,  # 假设是16位音频
            channels=1  # 单声道
        )

        # 使用 BytesIO 保存音频文件
        audio_file = io.BytesIO()
        audio_segment.export(audio_file, format="wav")
        audio_file.seek(0)

        # 识别音频
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                # 使用 Google Web API 进行转录
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Could not request results from Google Speech Recognition service; {e}"
    except Exception as e:
        return f"An error occurred: {e}"
