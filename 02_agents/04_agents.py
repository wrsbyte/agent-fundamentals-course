import asyncio
import os
from typing import Annotated

from pydantic import BaseModel, Field

from agents import Agent, Runner, function_tool, set_default_openai_key


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_default_openai_key(OPENAI_API_KEY)


class Weather(BaseModel):
    city: str = Field(description="El nombre de la ciudad")
    temperature_range: str = Field(
        description="El rango de temperatura en Celsius"
    )
    conditions: str = Field(description="Las condiciones meteorológicas")


@function_tool
def get_weather(
    city: Annotated[str, "La ciudad para la cual obtener el clima"]
) -> Weather:
    """Obtener la información meteorológica actual
    para una ciudad especificada.
    """
    print("[debug] get_weather called")
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Soleado y despejado",
    )


async def main():
    print("🚀 Agentes con OpenAI Agents SDK")

    agent = Agent(
        name="Agente del clima",
        instructions="Responde como un asistente del clima útil.",
        tools=[get_weather],
    )

    query = '¿Cual es el clima actual en Tokio?'
    print(f"🟩 Pregunta del usuario: {query}")
    result = await Runner.run(agent, input=query)

    print("🟩 Respuesta del agente:")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
