import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VECTOR_STORE_ID = "vs_690ed502e1d48191beed2e4f82c35992"
client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    pass


if __name__ == "__main__":
    main()
