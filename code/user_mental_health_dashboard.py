import gradio as gr
import json
import matplotlib.pyplot as plt
import numpy as np

def user_mental_health_dashboard():

    # 读取数据
    # filename = "../user_messages.json"  # 确保此文件路径正确
    # try:
    #     with open(filename, 'r', encoding='utf-8') as file:
    #         user_data = json.load(file)
    #         print(user_data)
    # except FileNotFoundError:
    #     return "Error: User data file not found."
    # except json.JSONDecodeError:
    #     return "Error: Failed to decode JSON."

    # 创建用户心理健康数据的 Markdown 摘要
    summary = "## Summary of your current mental health\n\n"

    # # 从助手中提取消息
    # assistant_messages = [item['content'] for item in user_data if item.get('role') == 'assistant']
    #
    # # 将助手消息附加到摘要中
    # if assistant_messages:
    #     summary += "**Assistant Messages:**\n"
    #     for message in assistant_messages:
    #         summary += f"- {message}\n"
    # else:
    #     summary += "No assistant messages available."

    return summary


def plot_anxiety_scale():
    # 模拟数据
    months = np.arange(1, 13)  # 1 到 12 个月
    scores = [0,0,0,0,0,0,0,0,20,0,0,0]  # 随机生成 0 到 20 之间的分数

    # 创建图表
    plt.figure(figsize=(10, 5))
    plt.plot(months, scores, marker='o', linestyle='-', color='b')
    plt.title('Zung Self-Rating Anxiety Scale over the Year')
    plt.xlabel('Month')
    plt.ylabel('Anxiety Score (0/20)')
    plt.xticks(months, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.ylim(0, 20)
    plt.grid()

    # 保存图表到文件
    plt.savefig('anxiety_scale.png')
    plt.close()  # 关闭图表以释放内存

    return 'anxiety_scale.png'