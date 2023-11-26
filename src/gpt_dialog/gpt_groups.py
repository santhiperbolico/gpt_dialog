from typing import List

from attr import attrs, attrib

from gpt_dialog.gpt_bot import ChatBotGPT


SYSTEM_MESSAGE_MODERATOR = """
Eres el responsable de tomar una decisión o dar una respuesta a una cuestión importante.
Para ello te has rodeado de varios asistentes que te van a dar pistas para dar una respuesta.
Después de escuharles te pedirán una respuesta.
"""

SYSTEM_MESSAGE_BOTS = "Pertenecéis a un grupo de expertos que tenéis que asesorar sobre una cuestión de una manera diversa."


@attrs
class ChatBotGroups:
    """
    Grupo de chatbots que van a generar un debate y luego lanzar una conclusión.
    """

    chatbot_list = attrib(type=List[ChatBotGPT], init=True, default=[])
    moderator = attrib(type=ChatBotGPT, init=False)

    def add_bot(
            self,
            name: str,
            model_type: str,
            system_message: str = None,
            api_key: str = None
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
        """
        chat_bot = ChatBotGPT(name)
        chat_bot.start_chat(model_type, system_message, api_key)
        self.chatbot_list.append(chat_bot)

    def launch_debate(
            self,
            question: str,
            model_type: str,
            system_message: str = None,
            api_key: str = None,
            iterations: str = 10,
            verbose: bool = False
    ):
        """
        Método que lanza un debate dada una cuestión y el moderado va a sacar una conclusión.

        Parameters
        ----------
        question: str
            Cuestión puesta en debate.
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        iterations: str, default 10
            Número de iteraciones que se lanza a preguntar a los asistentes.
        verbose: bool, default False
            Indica si se quiere imprimir los mensajes.

        Returns
        -------
        conclusion: str
            Conclusión alcanzada por el moderador.
        """
        self.moderator = ChatBotGPT("moderator")
        system_message = system_message or SYSTEM_MESSAGE_MODERATOR
        self.moderator.start_chat(model_type, system_message, api_key)
        self.init_bots(question, model_type, system_message, api_key)
        messages_list = []
        iteration_message = [
            {"role": "user", "content": "Comienza el debate con tu primera respuesta."}]
        for iteration in range(iterations):
            for bot in self.chatbot_list:
                content = bot.chat(iteration_message)
                content = f"El asistente {bot.name} dice: {content}"
                if verbose:
                    print(content)
                iteration_message.append({"role": "user", "content": content})
                if len(iteration_message) > len(self.chatbot_list) - 1:
                    iteration_message.remove(iteration_message[0])

            messages_list = messages_list + iteration_message

        messages_list = messages_list + [
            {"role": "user", "content": f"Qué conclusión sacas sobre la cuestión: {question}"}]
        conclusion = self.moderator.chat(messages_list)
        if verbose:
            print(f"Moderador: {conclusion}")
        return conclusion

    def init_bots(
            self,
            question: str,
            model_type: str,
            system_message: str = None,
            api_key: str = None
    ):
        """
        Método que inicializa los bots que van a debatir.

        Parameters
        ----------
        question: str
            Cuestión puesta en debate.
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY
        """
        for bot in self.chatbot_list:
            role = "user"
            if len(bot.list_messages) > 0:
                role = bot.list_messages[0].get("role", "user")
            content = f"{SYSTEM_MESSAGE_BOTS} La cuesión a debatir es: {question}"
            if role == "system":
                content = bot.list_messages[0].get("content")
                content = f"{content} {SYSTEM_MESSAGE_BOTS} La cuesión a debatir es: {question}"
            bot.start_chat(model_type, content, api_key)

    @classmethod
    def create_bots(
            cls,
            number: int,
            model_type: str,
            system_message: str = None,
            api_key: str = None
    ):
        """
        Método que crea un grupo de bots con el mismo patrón.

        Parameters
        ----------
        number: int
            Número de bots que se quieren generar.
        model_type: str
            Tipo de modelo de OpenAI
        system_message: str, default None
            Mensaje asociado al sistema del bot.
        api_key: str, default None
            API KEY de OpenAI. Por defecto toma la variable de entorno de OPENAI_API_KEY

        Returns
        -------
        group: ChatBotGroups
            Grupo de chatbots
        """
        group = ChatBotGroups([])
        for iteration in range(number):
            name = f"bot_{iteration}"
            group.add_bot(name, model_type, system_message, api_key)
        return group
