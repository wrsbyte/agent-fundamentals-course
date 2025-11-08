import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = "vs_690ed502e1d48191beed2e4f82c35992"
client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(input):
    response = client.responses.create(
        model="gpt-5-mini",
        input=input,
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
    if not messages:
        return None

    return messages[0].content[0].text


def main():
    pass


if __name__ == "__main__":
    main()
