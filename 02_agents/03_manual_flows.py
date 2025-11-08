import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = "vs_690ed502e1d48191beed2e4f82c35992"
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(input, conversation):
    response = client.responses.create(
        model="gpt-5-mini",
        input=input,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
            "max_num_results": 1
        }],
        conversation=conversation.id,
    )
    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if not messages:
        return None

    return messages[0].content[0].text


def workflow(user_input, conversation):
    """Análisis de sentimientos"""

    print("🟦 Analizando el sentimiento del mensaje...")
    mood = generate_response(
        "Analiza el siguiente texto y determina "
        "si el sentimiento es positivo, negativo o neutral:\n\n"
        f"Mensaje del usuario: {user_input}. "
        "Responde solo con una palabra: positivo, negativo o neutral."
        "Ejemplo de respuesta: { 'mood': 'positivo' }",
        conversation
    )

    print(f"🟦 Sentimiento: '{mood}'")

    if "negativo" in mood.lower():
        print("🟦 Proporcionando consejo...")
        advice = generate_response(
            "El mood del usuario es negativo. "
            "Proporciona un consejo breve y positivo "
            "para alguien que se siente triste o negativo. "
            "Usa el mensaje del usuario como inspiración.\n\n"
            f"Mensaje del usuario: {user_input}",
            conversation
        )
        return advice

    if "positivo" in mood.lower():
        print("🟦 Proporcionando cumplido...")
        compliment = generate_response(
            "El mood del usuario es positivo. "
            "Proporciona un cumplido breve y alegre "
            "para alguien que se siente feliz o positivo. "
            "Usa el mensaje del usuario como inspiración.\n\n"
            f"Mensaje del usuario: {user_input}",
            conversation
        )
        return compliment

    print("🟦 Proporcionando cita celebre...")
    neutral_response = generate_response(
        "El mood del usuario es neutral. "
        "Proporciona una cita celebre inspiradora. "
        "Usa el mensaje del usuario como temática.\n\n"
        f"Mensaje del usuario: {user_input}",
        conversation
    )
    return neutral_response


def main():
    print("🚀 Flujos de trabajo manuales")

    conversation = client.conversations.create(
        metadata={"topic": "Analisis de sentimientos"},
        items=[
            {
                "role": "system",
                "type": "message",
                "content": (
                    "Eres un agente que analiza el sentimiento "
                    "detrás de los mensajes del usuario y responde "
                    "de manera adecuada."
                ),
            }
        ],
    )

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Adiós!")
            break

        if not user_input.strip():
            print("Por favor, ingresa un mensaje válido.")
            continue

        result = workflow(user_input, conversation)
        print("Agente:", result)


if __name__ == "__main__":
    main()
