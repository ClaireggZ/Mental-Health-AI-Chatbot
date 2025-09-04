#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   chatgpt_bot.py
@Desc    :   call openAI api
"""
from openai import AzureOpenAI
import json

from user_guidance import user_info


class AzureChatGPT:
    def __init__(self, save_message=False):
        self.client = AzureOpenAI(
            azure_endpoint="https://witopenai.openai.azure.com",
            api_key="bac62700502a4ec98bde3e308d227efa",
            api_version="2024-05-01-preview",
        )
        self.model = "witDevp"
        self.messages = []

        print('user_guidance_result: {}'.format(user_info))
        self.init_message = [{"role": "system", "content": "Please act as an experienced and empathetic therapist to help assess my "
                                                           "anxiety levels. Use the Zung Self-Rating Anxiety Scale (SAS) to create a "
                                                           "personalized five-question scenario-based assessment. Each question should"
                                                           " describe a specific scenario, with each question worth 4 points for a total"
                                                           " score of 20. In each message, provide only one question, and after I answer"
                                                           " all five, give me a quantitative score. Make sure the questions are tailored"
                                                           " to my personality traits based on the assistant's previous messages, making "
                                                           "the assessment easier for me to understand. Before starting the first round, "
                                                           "give a very brief summary of my personality in a format like: 'Hi [Name]! From"
                                                           " the earlier assessment, we learned that you are a person who...' Also, please"
                                                           " adjust your tone to align with my personality traits."}]

        self.messages.append(self.init_message[0])
        self.save_message = save_message
        self.filename = "./user_messages.json"

    def ask_gpt(self):
        rsp = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        return rsp.choices[0].message.content

    def get_response(self, question):
        """ Call the OpenAI API to get a response.
        """
        # add user's question to message list
        self.messages.append({"role": "user", "content": question})

        # add user's description for the first time
        assistant_message = next((d for d in self.messages if d["role"] == "assistant"), None)
        if assistant_message is None:
            # add an assistant-role message
            self.messages.append({"role": "assistant", "content": user_info["user_description"]})

        print(json.dumps(self.messages, indent=2))

        # send questions
        rsp = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        answer = rsp.choices[0].message.content
        # add response to message list to preserve chat history
        self.messages.append({"role": "assistant", "content": answer})
        return answer

    def clean_history(self):
        self.messages.clear()
        self.messages.append(self.init_message[0])

    #TODO: 增加一个函数，可以将self.message存成一个本地文件的json
    def save_messages_to_file(self):
        """ Save self.messages to a local JSON file. """
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.messages, file, ensure_ascii=False, indent=4)
            print(f"Messages saved to {self.filename}.")
        except IOError as e:
            print(f"Error saving messages to file: {e}")
