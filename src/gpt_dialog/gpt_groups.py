import logging
from typing import Dict, List

from attr import attrib, attrs

from gpt_dialog.gpt_bot import ChatBotGPT


@attrs
class ChatBotGroups:
    """
    Grupo de chatbots que van a generar un debate y luego lanzar una conclusión.
    """

    moderator = attrib(type=ChatBotGPT, init=True, default=ChatBotGPT("moderator"))
    chatbot_list = attrib(type=List[ChatBotGPT], init=True, default=[])

    def add_bot(
        self,
        name: str,
        model_type: str,
        system_message: str = None,
        api_key: str = None,
        moderator_role: bool = False,
    ):
        """
        Método que añade un bot a la lista del rupo de bots.

        Parameters
        ----------
        name: str
            Nombre del bot.
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        moderator_role: bool, default False
            Indica si el role del bot es el de moderador.
        """
        if moderator_role:
            self.moderator = ChatBotGPT(name)
            self.moderator.start_chat(model_type, system_message, api_key)
            return None

        chat_bot = ChatBotGPT(name)
        chat_bot.start_chat(model_type, system_message, api_key)
        self.chatbot_list.append(chat_bot)

    def launch_debate(
        self,
        question: str,
        system_message: str = None,
        iterations: int = 10,
        verbose: bool = False,
    ) -> List[Dict[str, str]]:
        """
        Método que lanza un debate dada una cuestión devolviendo la conversación generada.

        Parameters
        ----------
        system_message
        question: str
            Cuestión puesta en debate.
        system_message: str
            Mensaje asociado al sistema del bot.
        iterations: int, default 10
            Número de iteraciones que se lanza a preguntar a los asistentes.
        verbose: bool, default False
            Indica si se quiere imprimir los mensajes.

        Returns
        -------
        message_list: List[Dict[str, str]]
            Lista con lso mensajes generados por el debate de bots..
        """

        self.init_bots(question, system_message)
        messages_list = []
        iteration_message = [{"role": "user", "content": question}]

        max_messages_iteration = len(self.chatbot_list)
        for iteration in range(iterations):
            for bot in self.chatbot_list:
                if len(iteration_message) > max_messages_iteration:
                    for _ in range(len(iteration_message) - max_messages_iteration):
                        iteration_message.remove(iteration_message[0])
                content = bot.chat(iteration_message)
                content = f"Assistant {bot.name}: {content}"
                if verbose:
                    logging.info("-> %s" % content)
                iteration_message.append({"role": "user", "content": content})

            max_messages_iteration = len(self.chatbot_list) - 1
            messages_list = messages_list + iteration_message
        return messages_list

    def get_conclusion(
        self,
        question: str,
        messages_list: List[Dict[str, str]] = None,
        model_type: str = None,
        system_message: str = None,
        api_key: str = None,
        remove_cache: bool = True,
    ) -> str:
        """
        Método que dada una lista con los mensajes sacados de un conjunto de bots
        realiza una conclusión del debate. Para crea un boto llamado moderador al cual
        se le pasará la cuestión a tratar y la lista de mensajes asociados.

        Parameters
        ----------
        question: str
            Pregunta o cuestión lanzada al moderador para extraiga una conclusión.
        model_type: str, defautl None
            Tipo del modelo usado en el cliente de OpenAI creado para el bot moderador.
            Por defecto se usa el moderador creado.
        messages_list: List[Dict[str, str]], default None
            Lista con los mensajes asociados al debate de bots. Pode defecto no pasa ningúna
            lista de mensajes.
        system_message: str, default None
            Mensaje asociado al sistema del bot moderador.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        remove_cache: bool, default True
            Indica si se quiere borrar la posible cache del moderador creando un nuevo
            bot llamada moderador.

        Returns
        -------
        conclusion: str
            Conclusión obtenida por el moderador
        """
        if remove_cache:
            bot_name = self.moderator.name
            model_type = model_type or self.moderator.model_type
            api_key = api_key or self.moderator.client.api_key
            system_message = system_message or self.moderator.list_messages[0].get("content")
            self.add_bot(bot_name, model_type, system_message, api_key, True)

        if messages_list is None:
            messages_list = []
        messages_list = messages_list + [{"role": "user", "content": question}]
        conclusion = self.moderator.chat(messages_list)
        logging.info("-> Moderador: %s" % conclusion)
        return conclusion

    def init_bots(self, question: str, system_message: str = None):
        """
        Método que inicializa los bots que van a debatir.

        Parameters
        ----------
        question: str
            Cuestión puesta en debate.
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        """
        system_message = system_message or ""
        system_question = f"{system_message} {question}".strip()
        for bot in self.chatbot_list:
            role = "user"
            if len(bot.list_messages) > 0:
                role = bot.list_messages[0].get("role", "user")
            system_content = ""
            if role == "system":
                system_content = bot.list_messages[0].get("content")
            bot.start_chat(
                model_type=bot.model_type,
                system_message=f"{system_content} {system_question}".strip(),
                api_key=bot.client.api_key,
            )

    @classmethod
    def create_bots(
        cls,
        number: int,
        model_type: str,
        system_message: str = None,
        system_message_moderator: str = None,
        api_key: str = None,
    ):
        """
        Método que crea un grupo de bots con el mismo patrón y genera un moderador de dicho
        grupo de bots.

        Parameters
        ----------
        number: int
            Número de bots que se quieren generar.
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        system_message_moderator: str, default None
            Mensaje asociado al bot moderador.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY

        Returns
        -------
        group: ChatBotGroups
            Grupo de chatbots
        """
        chatbot_list = []
        for iteration in range(number):
            name = f"bot_{iteration}"
            chat_bot = ChatBotGPT(name)
            chat_bot.start_chat(model_type, system_message, api_key)
            chatbot_list.append(chat_bot)
        chat_bot_moderator = ChatBotGPT("moderator")
        chat_bot_moderator.start_chat(model_type, system_message_moderator, api_key)
        return cls(moderator=chat_bot_moderator, chatbot_list=chatbot_list)
