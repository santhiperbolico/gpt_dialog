from typing import Callable
from unittest import mock

import pytest

from gpt_dialog.gpt_bot import ChatBotGPT
from gpt_dialog.gpt_groups import ChatBotGroups


def chat_mock(message) -> Callable[[str], str]:
    def init(m: str) -> str:
        return message

    return init


def test_create_bots():
    number_bots = 3
    group = ChatBotGroups.create_bots(
        number=number_bots,
        model_type="gpt-3.5-turbo",
        system_message="Es un ejemplo",
        system_message_moderator="Tu eres el moderador",
        api_key="*************",
    )
    assert isinstance(group, ChatBotGroups)
    assert len(group.chatbot_list) == number_bots
    for chatbot in group.chatbot_list:
        assert isinstance(chatbot, ChatBotGPT)
        assert "Es un ejemplo" == chatbot.list_messages[0].get("content")
    assert isinstance(group.moderator, ChatBotGPT)
    assert "Tu eres el moderador" == group.moderator.list_messages[0].get("content")


@pytest.mark.parametrize(
    "system_message, expected",
    [
        ("Que eres un test", "Es un ejemplo. Que eres un test ¿Es esto un test?"),
        (None, "Es un ejemplo. ¿Es esto un test?"),
    ],
)
def test_init_bots(system_message, expected):
    number_bots = 3
    group = ChatBotGroups.create_bots(
        number=number_bots,
        model_type="gpt-3.5-turbo",
        system_message="Es un ejemplo.",
        api_key="*************",
    )
    group.init_bots("¿Es esto un test?", system_message)
    for bot in group.chatbot_list:
        content = bot.list_messages[0].get("content")
        assert len(bot.list_messages) == 1
        assert content == expected


@mock.patch("gpt_dialog.gpt_bot.ChatBotGPT")
@mock.patch("gpt_dialog.gpt_bot.ChatBotGPT")
def test_launch_debate(chat_bot_gpt_mock_1, chat_bot_gpt_mock_2):
    message_1 = "Es una respuesta test del asistente 0"
    chatbot_mock_1 = chat_bot_gpt_mock_1.return_value
    chatbot_mock_1.chat = chat_mock(message_1)
    chatbot_mock_1.name = "bot_0"
    message_2 = "Es una respuesta test del asistente 1"
    chatbot_mock_2 = chat_bot_gpt_mock_2.return_value
    chatbot_mock_2.chat = chat_mock(message_2)
    chatbot_mock_2.name = "bot_1"
    chatbot_list_mock = [chatbot_mock_1, chatbot_mock_2]
    group = ChatBotGroups(chatbot_list=chatbot_list_mock)
    message_list = group.launch_debate("¿Esto es un test?", iterations=2)
    for i in range(4):
        expected_message = f"Assistant bot_{i%2}: Es una respuesta test del asistente {i%2}"
        message = message_list[i + 1]
        assert message.get("content") == expected_message
    assert message_list[0].get("content") == "¿Esto es un test?"
