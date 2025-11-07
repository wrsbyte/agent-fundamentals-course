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
        model="gpt-5-nano",
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
    function_calls = [
        c
        for c in response.output
        if c.type == "function_call"
    ]
    if function_calls:
        print(
            "OPEN AI Indica que hay que llamar a la función: ",
            function_calls[0].name
        )
        user = get_current_user()
        print("🔧 Función get_current_user() retornó: ", user)

    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if messages:
        print(
            "🤖 Respuesta normal (sin función): ",
            messages[0].content[0].text
        )


if __name__ == "__main__":
    main()
