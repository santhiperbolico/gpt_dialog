import os
from typing import Dict, List, Union

import openai
from attr import attrs, attrib


@attrs
class ChatBotGPT:
    """
    Clase que genera bots basados en modelos de GPT
    """

    name = attrib(type=str, init=True)
    model_type = attrib(type=str, init=False)
    client = attrib(type=openai.OpenAI, init=False)
    list_messages = attrib(type=List[Dict[str, str]], init=False)

    def start_chat(
            self,
            model_type: str,
            system_message: str = None,
            api_key: str = None
    ) -> None:
        """
        Método que limpia el histórico de la conversación y genera un nuevo bot.

        Parameters
        ----------
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        """
        self.list_messages = []
        if system_message:
            self.list_messages = [{"role": "system", "content": system_message}]
        self.model_type = model_type
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=api_key)

    def chat(self, message:  Union[List[Dict[str, str]], str]) -> str:
        """
        Método que le pasa un mensaje al bot generado.

        Parameters
        ----------
        message: Union[List[Dict[str, str]], str]
            Mensaje del usuario

        Returns
        -------
        assistant_message: str
            Mensaje devuelto por el asistente.
        """
        if isinstance(message, str):
            message = [{"role": "user", "content": message}]
        self.list_messages = self.list_messages + message
        completion = self.client.chat.completions.create(
            model=self.model_type,
            messages=self.list_messages
        )
        assistant_message = completion.choices[0].message.content
        self.list_messages.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def conversations(
            self, model_type: str = None,
            system_message: str = None,
            api_key: str = None,
            max_chats: int = 10000
    ) -> None:
        """
        Método que genera un bucle de convesación
        Parameters
        ----------
        model_type: str, default None
            Tipo de modelo de OpenAI. Si es None usa el modelo generado por start_chat.
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        max_chats: int, default 10000
            Máximas iteraciones del chat en la conversación.
        """
        if model_type:
            self.start_chat(model_type, system_message, api_key)

        for _ in range(max_chats):
            message = input("Tu: ")
            assistant_message = self.chat(message)
            print(f"Assistant {self.name}: {assistant_message}")
