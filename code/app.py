#!/usr/bin/env python

import gradio as gr
from azure_chatgpt import AzureChatGPT
from user_guidance import user_guidance
from voice_input import another_function
from user_mental_health_dashboard import plot_anxiety_scale

# 调用gpt的bot
chatgpt = AzureChatGPT()

# 全局变量，记录用户是否完成了问卷
is_assessment_completed = False

def predict(input, chatbot):
    """ 调用openai接口，获取答案
    """
    chatbot.append((input, ""))
    # 找chatgpt要答案
    response = chatgpt.get_response(input)
    chatgpt.save_messages_to_file()
    chatbot[-1] = (input, response)
    return chatbot

def reset_user_input():
    return gr.update(value='')

def reset_state():
    chatgpt.clean_history()
    return []

def chat_interface():
    with gr.Blocks() as chat_demo:
        chatbot = gr.Chatbot()
        with gr.Row():
            with gr.Column(scale=4):
                with gr.Column(scale=50):
                    user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10, container=False)
                with gr.Column(min_width=32, scale=1):
                    submitBtn = gr.Button("Submit", variant="primary")
            with gr.Column(scale=1):
                emptyBtn = gr.Button("Clear History")
        # 提交问题
        submitBtn.click(predict, [user_input, chatbot], [chatbot], show_progress=True)
        submitBtn.click(reset_user_input, [], [user_input])
        # 清空历史对话
        emptyBtn.click(reset_state, outputs=[chatbot], show_progress=True)

    return chat_demo


def main():
    with gr.Blocks() as demo:

        # 使用 State 变量保存问卷完成的状态，初始为 False
        assessment_completed = gr.State(False)

        with gr.Tabs() as tabs:
            with gr.Tab("Personal Assessment"):
                user_guidance(assessment_completed)

            # 让 Emotional Support 和 Another Function 初始不可见
            with gr.Tab("Emotional Support", visible=False) as tab1:
                chat_interface()

            with gr.Tab("Voice Emotional Support", visible=False) as tab2:
                another_function()

            with gr.Tab("User mental health dashboard", visible=False) as tab3:
                gr.Markdown("### Zung Self-Rating Anxiety Scale Over the Year")
                output_image = gr.Image(label="Anxiety Scale Chart")
                refresh_button = gr.Button("Generate Anxiety Scale Chart")

                # 生成图表的函数
                def generate_chart():
                    return plot_anxiety_scale()

                # 按钮点击后更新图像
                refresh_button.click(generate_chart, outputs=output_image)

        # Control the visibility of tabs using State
        assessment_completed.change(
            fn=lambda completed: (
                gr.update(visible=completed),  # For Emotional Support tab
                gr.update(visible=completed),  # For Voice Emotional Support tab
                gr.update(visible=completed)   # For User Mental Health Dashboard tab
            ),
            inputs=[assessment_completed],
            outputs=[tab1, tab2, tab3]  # Ensure three outputs are provided
        )

    demo.launch(share=False, inbrowser=True)

if __name__ == '__main__':
    main()