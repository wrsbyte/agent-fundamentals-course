from openai import OpenAI
from openai.types.responses import (
    EasyInputMessageParam, ResponseOutputMessageParam
)
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def send_message_to_chat(user_input, history=[]):
    user_message = EasyInputMessageParam(
        role="user",
        type="message",
        content=user_input,
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=history + [user_message],
    )

    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]

    if not messages:
        return "-- No response --"

    assistance_message_text = messages[0].content[0].text
    assistance_message = ResponseOutputMessageParam(
        role="assistant",
        type="message",
        content=assistance_message_text,
    )

    return user_message, assistance_message


def main():
    print("🚀 Conversación manual en bucle...")
    SYSTEM_PROMPT = (
        "Actua como si fueras El Chavo del 8, responde como él."
        "Únicamente habla sobre el vecindario y sus amigos. "
        "Tener en cuenta toda la información de la serie de televisión "
        "El Chavo del 8 para responder de manera auténtica."
    )
    history = [
        EasyInputMessageParam(
            role="system",
            type="message",
            content=SYSTEM_PROMPT,
        )
    ]

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Adiós!")
            break

        user_message, assistance_message = send_message_to_chat(
            user_input,
            history
        )

        print("El Chavo:", assistance_message["content"])

        history.append(user_message)
        history.append(assistance_message)

    print("✅ Conversación terminada.")
    print(" # Historial completo de la conversación:")

    for msg in history:
        if msg['role'] == "system":
            print(" - Sistema:", msg["content"])
        elif msg['role'] == "user":
            print(" - Tú:", msg["content"])
        else:
            print(" - El Chavo:", msg["content"])


if __name__ == "__main__":
    main()
