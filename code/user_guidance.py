import gradio as gr
from datetime import datetime

user_info = {
    "nickname": "",
    "assessment_score": 80,
    "assessment_date": datetime.now().date(),
    "user_description": ""
}

questions = [
    # Thinking or Feeling
    {"label": "When making decisions, I tend to:",
     "choices": [("A. 📊Rely on logic and data", "A"),
                 ("B. 🫀Rely on intuition and feelings", "B")]
     },
    # Sensing or Intuition
    {"label": "When faced with a new task, I focus more on:",
     "choices": [("A. 🔧How to efficiently complete it", "A"),
                 ("B. 🧠The meaning and value of the task", "B")]
     },
    # Introversion or Extroversion
    {"label": "In social situations, I usually:",
     "choices": [("A. 🙋🏼‍♀️Actively engage in conversations", "A"),
                 ("B. 👀Prefer to listen to others", "B")]
     },
    # Judging or Perceiving
    {"label": "When making plans, I usually:",
     "choices": [("A. ✍🏻Set detailed steps", "A"),
                 ("B. 🤸🏼‍♀️Stay flexible and adjust as needed", "B")]
     },
    # Results-oriented or process-oriented
    {"label": "In work, I value more:",
     "choices": [("A. ☑️Results and efficiency", "A"),
                 ("B. 🔀Process and experience", "B")]
     },
    # Agreeableness in the Big Five personality traits
    {"label": "Regarding others' emotional needs, I usually: ",
     "choices": [("A. 🙎🏻‍♀️Rarely consider them", "A"),
                 ("B. 💁🏻‍♀️Pay close attention to them", "B")]
     },
]


def format_introduction(name, age, answers):
    global user_info
    result = "My name is {}. I am {} years old. This is a series of descriptions of my personality: ".format(name, age)
    for index, answer in enumerate(answers, start=0):
        question = questions[index]
        choices = question["choices"]
        chosen_option = next((d for d in choices if d[1] == answer), None)
        another_option = next((d for d in choices if d[1] != answer), None)
        result += "{} {} instead of {}; ".format(question["label"], chosen_option[0], another_option[0])

    return result

def user_guidance(assessment_completed):
    with gr.Blocks() as guidance_demo:
        gr.Markdown("## Introduce Yourself😆")
        name = gr.Textbox(label="Your nickname", placeholder="please input your nickname")
        age = gr.Textbox(label="Your age", placeholder="please input your age")

        # render radio components for questions
        radio_list = []
        for index, question in enumerate(questions, start=0):
            radio_list.append(gr.Radio(label=question["label"], choices=question["choices"]))

        submit = gr.Button("Submit")
        completion_message = gr.Markdown(visible=False)  # display thank you information

        # callback function after submit
        def handle_submission(name, age, *answers):
            message = f"Thank you for your response {name}! Your age is {age}. \n" \
                      "We’ve got a good understanding of your personality," \
                      " and we will create a scale for you based on this information."

            user_info["user_description"] = format_introduction(name, age, answers)
            user_info["nickname"] = name

            return gr.update(value=message, visible=True), True  # return True to update assessment_completed

        # callback function to update assessment_completed and display thank you information
        submit.click(handle_submission, [name, age, *radio_list],
                     [completion_message, assessment_completed])

    return guidance_demo
