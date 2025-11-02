#!/usr/bin/env python3
"""
Memory en Agentes - Clase 6

Demuestra diferentes tipos de memoria en LangChain:
1. ConversationBufferMemory (guarda todo)
2. ConversationSummaryMemory (resume periódicamente)
3. ConversationBufferWindowMemory (ventana deslizante)
"""

import os

from dotenv import load_dotenv

load_dotenv()

from langchain.chains import ConversationChain
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory,
)
from langchain_anthropic import ChatAnthropic
from rich.console import Console
from rich.panel import Panel

console = Console()

def ejemplo_1_buffer_memory():
    """Buffer Memory - Guarda toda la conversación"""
    console.print("\n[bold blue]═══ Ejemplo 1: ConversationBufferMemory ═══[/bold blue]\n")

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    memory = ConversationBufferMemory()

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    # Conversación
    messages = [
        "Hola, me llamo Carlos y soy desarrollador Python",
        "¿Cuál es mi nombre?",
        "¿Qué lenguaje de programación uso?"
    ]

    for msg in messages:
        console.print(f"[yellow]User:[/yellow] {msg}")
        response = conversation.predict(input=msg)
        console.print(f"[green]Assistant:[/green] {response}\n")

    # Mostrar memoria
    console.print(Panel(
        memory.buffer,
        title="[cyan]Memoria Completa (Buffer)[/cyan]",
        border_style="cyan"
    ))


def ejemplo_2_summary_memory():
    """Summary Memory - Resume conversaciones largas"""
    console.print("\n[bold blue]═══ Ejemplo 2: ConversationSummaryMemory ═══[/bold blue]\n")

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
    memory = ConversationSummaryMemory(llm=llm)

    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    # Simular conversación larga
    messages = [
        "Hola, estoy trabajando en un proyecto de ML con Python",
        "Uso FastAPI para la API y PostgreSQL para la base de datos",
        "Tengo problemas con queries lentas en la DB",
        "¿De qué hemos hablado hasta ahora?"
    ]

    for msg in messages:
        console.print(f"[yellow]User:[/yellow] {msg}")
        response = conversation.predict(input=msg)
        console.print(f"[green]Assistant:[/green] {response}\n")

    # Mostrar resumen de la memoria
    console.print(Panel(
        memory.buffer,
        title="[magenta]Resumen de Conversación[/magenta]",
        border_style="magenta"
    ))


def ejemplo_3_window_memory():
    """Window Memory - Solo últimos N mensajes"""
    console.print("\n[bold blue]═══ Ejemplo 3: ConversationBufferWindowMemory ===[/bold blue]\n")

    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)

    # Mantener solo últimos 2 mensajes (1 intercambio)
    memory = ConversationBufferWindowMemory(k=2)

    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    messages = [
        ("Mensaje 1", "Mi nombre es Ana"),
        ("Mensaje 2", "Trabajo como arquitecta de software"),
        ("Mensaje 3", "Me especializo en microservicios"),
        ("Pregunta", "¿Cuál es mi nombre?")  # Debería haber olvidado esto
    ]

    for i, (label, msg) in enumerate(messages, 1):
        console.print(f"[yellow]{label}:[/yellow] {msg}")
        response = conversation.predict(input=msg)
        console.print(f"[green]Assistant:[/green] {response}\n")

        if i == 3:
            console.print("[dim]ℹ️  Window memory solo mantiene últimos 2 mensajes[/dim]\n")

    # Mostrar memoria (solo últimos 2 mensajes)
    console.print(Panel(
        memory.buffer,
        title="[red]Memoria (Ventana: últimos 2 mensajes)[/red]",
        border_style="red"
    ))


def main():
    console.print(Panel.fit(
        "[bold cyan]LangChain Memory - Tipos de Memoria[/bold cyan]\n"
        "Comparación de Buffer, Summary y Window Memory",
        border_style="cyan"
    ))

    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY no configurada")
        return

    try:
        ejemplo_1_buffer_memory()
        input("\n[dim]Presiona Enter...[/dim]\n")

        ejemplo_2_summary_memory()
        input("\n[dim]Presiona Enter...[/dim]\n")

        ejemplo_3_window_memory()

        console.print("\n[bold green]✓ Ejemplos completados![/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    main()
