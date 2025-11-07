from openai import OpenAI
import os


def main():
    print("🚀 Respuestas con razonamiento...")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "Reflexiona sobre la bibliografía de Borges, y"
        " explica cuál sería el libro indicado para niños de 12 años."
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="o3-mini",
        input=prompt,
        reasoning={
            "effort": "high"
        }
    )

    print("🔍 Respuesta de OpenAI:")
    print(response, end="\n\n")

    print("✅ Output completo.")

    # reasoning = [
    #     m
    #     for m in response.output
    #     if m.type == "reasoning"
    # ]
    # if reasoning:
    #     print("Razonamiento: ", reasoning[0].content[0].text)

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
