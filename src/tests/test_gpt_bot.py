from datetime import datetime
from unittest import mock

import pytest
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice

from gpt_dialog.gpt_bot import ChatBotGPT


@pytest.fixture
def chatbot():
    name = "bot_test"
    model = "gpt-3.5-turbo"
    system_message = "Eres un chat creado para un test"
    api_key = "**************"
    chatbot = ChatBotGPT(name=name)
    chatbot.start_chat(model, system_message=system_message, api_key=api_key)
    return chatbot


def test_create_chatbot(chatbot):
    system_message = "Eres un chat creado para un test"
    assert chatbot.list_messages == [{"role": "system", "content": system_message}]
    assert isinstance(chatbot.client, OpenAI)


@mock.patch("gpt_dialog.gpt_bot.openai.OpenAI")
def test_chat(openai_client_class_mock, chatbot):
    expected_message = "Es una respuesta test"
    chatcompletion_mock = ChatCompletion(
        id="foo",
        model="gpt-3.5-turbo",
        object="chat.completion",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content=expected_message,
                    role="assistant",
                ),
            )
        ],
        created=int(datetime.now().timestamp()),
    )
    openai_client_mock = openai_client_class_mock.return_value
    openai_client_mock.chat.completions.create.return_value = chatcompletion_mock
    chatbot.client = openai_client_mock
    result = chatbot.chat("Esta consulta es de prueba?")
    assert result == expected_message
    assert len(chatbot.list_messages) == 3
    assert chatbot.list_messages[1] == {"role": "user", "content": "Esta consulta es de prueba?"}
    assert chatbot.list_messages[2] == {"role": "assistant", "content": expected_message}
