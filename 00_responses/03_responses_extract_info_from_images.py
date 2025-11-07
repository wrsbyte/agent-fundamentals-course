from openai import OpenAI
import os


def main():
    print("🚀 Usando la api de imágenes")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    prompt = (
        "De la siguiente imagen, explica qué es, y si aplica,"
        "indica que está haciendo, y dónde, el protagonista de la foto."
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": "https://img.freepik.com/free-photo/panda-bear-leaning-against-tree-eating-bamboo-shoots_493961-7.jpg"
                    }
                ]
            }
        ],
    )

    print("🔍 Respuesta de la API de OpenAI:")
    print(response, end="\n\n")

    print("✅ Output completo.")
    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if messages:
        print("Respuesta: ", messages[0].content[0].text)


if __name__ == "__main__":
    main()
