import os
from openai import OpenAI
from openai.types.responses import (
    EasyInputMessageParam, ResponseOutputMessageParam
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def send_message_to_chat(user_input, conversation):
    user_message = EasyInputMessageParam(
        role="user",
        type="message",
        content=user_input,
    )
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[user_message],
        conversation=conversation.id,
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
    print("🚀 Conversación con librería de OpenAI...")

    SYSTEM_PROMPT = (
        "Actua como si fueras Sherlock Holmes, responde como él."
        "Únicamente habla sobre sus casos y su vida."
        "Tener en cuenta toda la información de los libros y adaptaciones "
        "de Sherlock Holmes para responder de manera auténtica."
    )
    system_message = EasyInputMessageParam(
        role="system",
        type="message",
        content=SYSTEM_PROMPT,
    )
    conversation = client.conversations.create(
        metadata={"topic": "Sherlock Holmes"},
        items=[
            system_message
        ],
    )

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Adiós!")
            break

        user_message, assistance_message = send_message_to_chat(
            user_input,
            conversation
        )

        print("SH:", assistance_message["content"])

    conversation = client.conversations.items.list(
        conversation.id,
        limit=100,
    )
    print("✅ Conversación terminada.")
    print(" # Historial completo de la conversación:")

    for msg in conversation.data:
        if msg.role == "system":
            print(" - Sistema:", msg.content[0].text)
        elif msg.role == "user":
            print(" - Tú:", msg.content[0].text)
        else:
            print(" - Sherlock Holmes:", msg.content[0].text)


if __name__ == "__main__":
    main()
