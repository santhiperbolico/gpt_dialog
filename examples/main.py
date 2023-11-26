import logging
import os

from dotenv import load_dotenv

from gpt_dialog.gpt_bot import ChatBotGPT
from gpt_dialog.gpt_groups import ChatBotGroups

load_dotenv("../src/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NUMBER = 2
MODEL_TYPE = "gpt-3.5-turbo"
ITERATIONS = 1

SYSTEM_MESSAGE_MODERATOR = """
Eres el responsable de tomar una decisión o dar una respuesta a una cuestión importante.
Para ello te has rodeado de varios asistentes que te van a dar pistas para dar una respuesta.
Después de escuharles te pedirán una respuesta sobre una cuestión.
"""

SYSTEM_MESSAGE_BOTS = (
    "Pertenecéis a un grupo de expertos que tenéis que asesorar "
    "sobre la siguiente cuestión de una manera diversa:"
)

SYSTEM_MESSAGE_CONTROL_BOT = (
    "Eres un experto consultado sobre un problema crucial, "
    "necesitamos que nos des una respuesta."
)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] [%(asctime)s] %(message)s")
    question = input("¿Qué quieres debatir?: ")

    bot = ChatBotGPT("Control")
    bot.start_chat(
        MODEL_TYPE,
        SYSTEM_MESSAGE_CONTROL_BOT,
        OPENAI_API_KEY,
    )
    conclusion_bot = bot.chat(question)
    logging.info("Control: %s \n" % conclusion_bot)

    group = ChatBotGroups.create_bots(
        number=NUMBER,
        model_type=MODEL_TYPE,
        system_message=SYSTEM_MESSAGE_BOTS,
        system_message_moderator=SYSTEM_MESSAGE_MODERATOR,
        api_key=OPENAI_API_KEY,
    )

    message_list = group.launch_debate(question=question, iterations=ITERATIONS, verbose=True)

    conclusion = group.get_conclusion(
        question=question,
        messages_list=message_list,
    )
