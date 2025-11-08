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
    print("🚀 Conversación manual con Mem0...")

    # https://docs.mem0.ai/open-source/overview


if __name__ == "__main__":
    main()
