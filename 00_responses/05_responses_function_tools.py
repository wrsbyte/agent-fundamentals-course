from openai import OpenAI
import os
import random


def get_current_user():
    return {
        "id": random.randint(1000, 9999),
        "username": 'wrs',
    }


def main():
    print("🚀 Creando herramientas personalizadas")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # prompt = (
    #     "¿Sabe cual es la capital de Francia?"
    # )
    prompt = (
        "Obtén la información del usuario actualmente logueado."
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{
            "type": "function",
            "name": "get_current_user",
            "description": "Get the current logged in user",
        }],
        input=prompt,
    )

    print("🔍 Respuesta de la API de OpenAI:")
    print(response, end="\n\n")

    print("✅ Output completo.")
    if response.output[0].type == "function_call":
        print(
            "OPEN AI Indica que hay que llamar a la función: ",
            response.output[0].name
        )
        user = get_current_user()
        print("🔧 Función get_current_user() retornó: ", user)
    else:
        print(
            "🤖 Respuesta normal (sin función): ",
            response.output[0].content[0].text
        )


if __name__ == "__main__":
    main()
