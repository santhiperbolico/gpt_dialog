# GPT Dialog

El paquete `gpt_dialog` facilita la creación de bots basados en modelos GPT capaces de dialogar entre sí. Los bots pueden discutir sobre un tema específico, y uno de ellos, denominado moderador, tiene la capacidad de generar una conclusión después de escuchar a los demás bots.

## Instalación

Para instalar el paquete, clona el repositorio y crea un entorno virtual. Asegúrate de tener Python 3.10 instalado en tu entorno.

# Requisitos
El paquete `gpt_dialog` requiere las siguientes librerías:

* `openai`
* `attrs`
* `python-dotenv`
Puedes instalar estos requisitos utilizando el siguiente comando:
```bash
pip install -r src/requirements.txt
```

Además, necesitarás una API key de OpenAI para utilizar el paquete. Asegúrate de configurar tu API key correctamente antes de utilizar el paquete.

# Uso

```python
from gpt_dialogs.gpt_groups import ChatBotGroups

group = ChatBotGroups.create_bots(NUMBER_BOTS, MODEL_TYPE, None, OPENAI_API_KEY)
question = input("¿Qué quieres debatir?: ")
conclusion = group.launch_debate(
    question, MODEL_TYPE, None, OPENAI_API_KEY, ITERATIONS, True)
```
Este es un ejemplo básico de cómo usar el paquete. Asegúrate de consultar la documentación para obtener información detallada sobre las funciones y opciones disponibles.

## Autor

  - **Santiago Arran Sanz**
    ([santhiperbolico](https://github.com/santhiperbolico/))