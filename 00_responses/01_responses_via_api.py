import requests
import os
import json


def main():
    print("🚀 Ejecutando la llamada a la API de OpenAI...")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    prompt = (
        "En español, redacta dos estrofas de un poema famoso, "
        "firmado por su autor, con el nombre del poema."
        "Libre de derechos de autor."
    )
    data = {
        "model": "gpt-5-mini",
        "input": prompt,
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    print("🔍 Respuesta de OpenAI:")
    print(json.dumps(data, indent=4))

    print("✅ Output completo.")

    # Obtener solo el texto de la respuesta
    print(data['output'][1]['content'][0]['text'])


if __name__ == "__main__":
    main()
