import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = "vs_690ed502e1d48191beed2e4f82c35992"
client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    print("🚀 Bases de datos vectoriales y RAG Manuales")

    query = "¿Quién es la persona con más seguidores en Instagram en 2025?"
    query = "¿Quién es la persona con menos seguidores en Instagram en 2025?"
    query = "¿Quien es el país con más PIB en 2025?"
    query = "¿Que localidad tiene el menor PIB en 2025?"

    prompt = f"""
    Usa la siguiente información para responder la pregunta de manera concisa:

    Pregunta:
    {query}
    """

    print("🚀 Enviando prompt a OpenAI:")
    print(prompt)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
            "max_num_results": 1
        }],
    )
    messages = [
        m
        for m in response.output
        if m.type == "message"
    ]
    if messages:
        print("\n\n🟩 Respuesta: ", messages[0].content[0].text)


if __name__ == "__main__":
    main()
