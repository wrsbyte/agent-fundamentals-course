import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def main():
    print("🚀 Bases de datos vectoriales y RAG")


if __name__ == "__main__":
    main()
