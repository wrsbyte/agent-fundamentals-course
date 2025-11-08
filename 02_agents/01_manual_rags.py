import os
from pathlib import Path
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = "vs_690ed502e1d48191beed2e4f82c35992"
client = OpenAI(api_key=OPENAI_API_KEY)


def create_vector_db():
    print("🚀 Creando o recuperando Vector Store...")

    # Uso de Vector Stores para RAG:
    # https://i0.wp.com/blog.voyageai.com/wp-content/uploads/2023/10/Untitled201.png?resize=1024%2C321&quality=80&ssl=1

    try:
        saved_store = client.vector_stores.retrieve(
            vector_store_id=VECTOR_STORE_ID
        )
        if saved_store:
            return saved_store
    except Exception:
        pass

    store = client.vector_stores.create(
        name="Paises y seguidores",
        description=(
            "Listado de países por PIB y personas "
            "con más seguidores en Instagram en 2025"
        ),
        metadata={},
    )

    print("🚀 Store creada:", store.id)

    # create embeddings and save to vector store
    client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=store.id,
        files=[
            Path("docs/seguidores_usuarios.txt"),
            Path("docs/pib_paises_mundo.txt"),
        ]
    )

    print("✅ Vector Store poblada con datos.")

    return store


def search_in_vector_store(store, query):
    print("🚀 Buscando en Vector Store...", query)
    response = client.vector_stores.search(
        vector_store_id=store.id,
        query=query,
        max_num_results=1
    )
    print("✅ Búsqueda completada. Resultados:", len(response.data))
    return "\n".join(
        [item.content[0].text for item in response.data]
    )


def main():
    print("🚀 Bases de datos vectoriales y RAG Manuales")

    store = create_vector_db()

    query = "¿Quién es la persona con más seguidores en Instagram en 2025?"
    query = "¿Quién es la persona con menos seguidores en Instagram en 2025?"
    query = "¿Quien es el país con más PIB en 2025?"
    query = "¿Que localidad tiene el menor PIB en 2025?"

    query_response = search_in_vector_store(store, query)

    prompt = f"""
    Usa la siguiente información para responder la pregunta de manera concisa:

    Contexto:
    {query_response}

    Pregunta:
    {query}
    """

    print("🚀 Enviando prompt a OpenAI:")
    print(prompt)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
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
