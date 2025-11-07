from openai import OpenAI
import os


def main():
    print("🚀 Buscando información en la web con OPEN AI")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "¿Cuales son los últimos titulares del New York Times?"
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )

    print("🔍 Respuesta de OpenAI:")
    print(response, end="\n\n")

    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if messages:
        message = messages[0]
        print("Respuesta: ", message.content[0].text)

        print("✅ Output completo. output len", len(response.output))
        print("Respuesta: ", message.content[0].text)
        print(
            "Número de fuentes usadas. ", len(
                message.content[0].annotations
            )
        )


if __name__ == "__main__":
    main()
