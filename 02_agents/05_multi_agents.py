from __future__ import annotations as _annotations

import asyncio
import random
import uuid
import os

from pydantic import BaseModel

from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions.visualization import draw_graph

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    handoff,
    trace,
    set_default_openai_key,
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set_default_openai_key(OPENAI_API_KEY)

# CONTEXT


class AirlineAgentContext(BaseModel):
    passenger_name: str | None = None
    confirmation_number: str | None = None
    seat_number: str | None = None
    flight_number: str | None = None


# TOOLS


@function_tool(
    name_override="faq_lookup_tool",
    description_override="Busca respuestas a preguntas frecuentes sobre la aerolínea."
)
async def faq_lookup_tool(question: str) -> str:
    question_lower = question.lower()
    if any(
        keyword in question_lower
        for keyword in ["bag", "baggage", "luggage", "carry-on", "hand luggage", "hand carry"]
        for keyword in ["bolsa", "equipaje", "maleta", "de mano", "equipaje de mano", "peso"]
    ):
        return (
            "Tu puedes llevar una maleta en el avión. "
            "Debe pesar menos de 23 kilogramos y medir 56 cm x 36 cm x 23 cm."
        )
    elif any(
        keyword in question_lower
        for keyword in ["asiento", "asientos", "ubicación", "avión"]
    ):
        return (
            "Hay 120 asientos en el avión. "
            "Hay 22 asientos en clase ejecutiva y 98 en clase económica. "
            "Las filas de salida son las filas 4 y 16. "
            "Las filas 5-8 son Economy Plus, con espacio adicional para las piernas. "
        )
    elif any(
        keyword in question_lower
        for keyword in ["wifi", "internet", "inalámbrico", "conectividad", "red", "en línea"]
    ):
        return "Tenemos wifi gratuito en el avión, únase a Airline-Wifi"
    return "Lo siento, no sé la respuesta a esa pregunta."


@function_tool
async def update_seat(
    context: RunContextWrapper[AirlineAgentContext], confirmation_number: str, new_seat: str
) -> str:
    """
    Actualiza el asiento para un número de confirmación dado.

    Args:
        confirmation_number: El número de confirmación del vuelo.
        new_seat: El nuevo asiento al que se actualizará.
    """
    # Update the context based on the customer's input
    context.context.confirmation_number = confirmation_number
    context.context.seat_number = new_seat
    # Ensure that the flight number has been set by the incoming handoff
    assert context.context.flight_number is not None, "Número de vuelo no requerido"

    return f"Se actualizó el asiento a {new_seat} para el número de confirmación {confirmation_number}"


# HOOKS


async def on_seat_booking_handoff(context: RunContextWrapper[AirlineAgentContext]) -> None:
    flight_number = f"WRS-{random.randint(100, 999)}"
    context.context.flight_number = flight_number


# AGENTS

faq_agent = Agent[AirlineAgentContext](
    name="Agente FAQ",
    handoff_description="Un agente útil que puede responder preguntas sobre la aerolínea.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Eres un agente de preguntas frecuentes. Si estás hablando con un cliente, probablemente fuiste transferido desde el agente de triaje.
    Usa la siguiente rutina para apoyar al cliente.
    # Rutina
    1. Identifica la última pregunta hecha por el cliente.
    2. Usa la herramienta de búsqueda de preguntas frecuentes para responder la pregunta. No confíes en tu propio conocimiento.
    3. Si no puedes responder la pregunta, transfiere de vuelta al agente de triaje.""",
    tools=[faq_lookup_tool],
)

seat_booking_agent = Agent[AirlineAgentContext](
    name="Agente de reserva de asientos",
    handoff_description="Un agente útil que puede actualizar un asiento en un vuelo.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Eres un agente de reserva de asientos. Si estás hablando con un cliente, probablemente fuiste transferido desde el agente de triaje.
    Usa la siguiente rutina para apoyar al cliente.
    # Rutina
    1. Pregunta por su número de confirmación.
    2. Pregunta al cliente cuál es su número de asiento deseado.
    3. Usa la herramienta de actualización de asiento para actualizar el asiento en el vuelo.
    Si el cliente hace una pregunta que no está relacionada con la rutina, transfiere de vuelta al agente de triaje.""",
    tools=[update_seat],
)

triage_agent = Agent[AirlineAgentContext](
    name="Agente de triaje",
    handoff_description="Un agente de triaje que puede delegar la solicitud de un cliente al agente apropiado.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    Eres un agente de triaje útil. Puedes usar tus herramientas para delegar preguntas a otros agentes apropiados.
    """,
    handoffs=[
        faq_agent,
        handoff(agent=seat_booking_agent, on_handoff=on_seat_booking_handoff),
    ],
)

faq_agent.handoffs.append(triage_agent)
seat_booking_agent.handoffs.append(triage_agent)


# RUN


async def main():
    current_agent: Agent[AirlineAgentContext] = triage_agent
    input_items: list[TResponseInputItem] = []
    context = AirlineAgentContext()

    # Generar y mostrar el gráfico del agente
    # Instalar: https://graphviz.org/download/
    # draw_graph(triage_agent, 'docs/05_multi_agents_agent_graph.png')
    # return

    # Normalmente, cada entrada del usuario sería una solicitud API a tu aplicación, y puedes envolver la solicitud en un trace()
    # Aquí, usaremos un UUID aleatorio para el ID de la conversación
    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Adiós!")
            break

        with trace("Customer service", group_id=conversation_id):
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=context)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(
                        f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(
                        f"Delegado desde {new_item.source_agent.name} a {new_item.target_agent.name}"
                    )
                elif isinstance(new_item, ToolCallItem):
                    print(f"{agent_name}: Llamando a una herramienta")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(
                        f"{agent_name}: Salida de la llamada a la herramienta: {new_item.output}")
                else:
                    print(
                        f"{agent_name}: Ignorando elemento: {new_item.__class__.__name__}")
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())
