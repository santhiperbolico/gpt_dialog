import os

from dotenv import load_dotenv

from gpt_dialog.gpt_bot import ChatBotGPT
from gpt_dialog.gpt_groups import ChatBotGroups

load_dotenv("../src/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NUMBER = 4
MODEL_TYPE = "gpt-3.5-turbo"
ITERATIONS = 2

if __name__ == "__main__":
    question = input("¿Qué quieres debatir?: ")

    bot = ChatBotGPT("Control")
    bot.start_chat(
        MODEL_TYPE,
        "Eres un experto consultado sobre un problema crucial, "
        "necesitamos que nos des una respuesta.",
        OPENAI_API_KEY,
    )
    conclusion_bot = bot.chat(question)
    print("Control: ", conclusion_bot, "\n")

    group = ChatBotGroups.create_bots(NUMBER, MODEL_TYPE, None, OPENAI_API_KEY)

    conclusion = group.launch_debate(question, MODEL_TYPE, None, OPENAI_API_KEY, ITERATIONS, True)
