import openai
import re
import httpx

class Chatbot:
    def __init__(self,system = ""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({'role':'system','content':system})
        
    def __call__(self,messages):
        self.messages.append({'role':'user','content':message})
        result = self.execute()
        self.messages.append({'role':'assistant','content':result})
        return result
    
    def execute(self):
        completion = openai.ChatCompletion.create(model = 'gpt-3.5-turbo',messages=self.messages)
        return completion.choices[0].message.content