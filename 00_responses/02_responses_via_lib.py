from openai import OpenAI
import os


def main():
    print("🚀 Ejecutando la llamada a la librería de OPEN AI...")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "En español, redacta dos estrofas de un poema famoso, "
        "firmado por su autor, con el nombre del poema."
        "Libre de derechos de autor."
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
    )

    print("🔍 Respuesta de la API de OpenAI:")
    print(response, end="\n\n")

    print("✅ Output completo.")

    # Obtener solo el texto de la respuesta
    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if messages:
        print("Respuesta: ", messages[0].content[0].text)


if __name__ == "__main__":
    main()
