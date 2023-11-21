import os

from dotenv import load_dotenv

from gpt_dialogs.gpt_groups import ChatBotGroups

load_dotenv("../src/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NUMBER = 3
MODEL_TYPE = "gpt-3.5-turbo"
ITERATIONS = 1

if __name__ == "__main__":
    group = ChatBotGroups.create_bots(NUMBER, MODEL_TYPE, None, OPENAI_API_KEY)
    question = input("¿Qué quieres debatir?: ")
    conclusion = group.launch_debate(
        question, MODEL_TYPE, None, OPENAI_API_KEY, ITERATIONS, True)
