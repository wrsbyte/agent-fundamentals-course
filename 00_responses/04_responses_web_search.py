from openai import OpenAI
import os


def main():
    print("🚀 Buscando información en la web con OPEN AI")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "¿Cuál es la hora y fecha actual en Tokio, Japón? "
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )

    print("🔍 Respuesta de la API de OpenAI:")
    print(response, end="\n\n")

    print("✅ Output completo.")
    print("Respuesta: ", response.output[1].content[0].text)
    print("Cita de: ", response.output[1].content[0].annotations[0].url)


if __name__ == "__main__":
    main()
