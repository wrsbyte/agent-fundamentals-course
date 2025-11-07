from openai import OpenAI
import os


def main():
    print("🚀 Ejecutando la llamada a la librería de OPEN AI...")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "En español, redacta seis estrofas de un poema famoso, "
        "firmado por su autor, con el nombre del poema. "
        "Libre de derechos de autor."
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        stream=True,
    )

    print("🔍 Respuesta de la API de OpenAI:")

    event_count = 0
    for chunk in response:
        if chunk.type == "response.output_text.delta":
            print(f"{chunk.delta}", end="",)
        event_count += 1

    print("✅ Output completo.")
    print(f"Total de eventos recibidos en el stream: {event_count}")


if __name__ == "__main__":
    main()
