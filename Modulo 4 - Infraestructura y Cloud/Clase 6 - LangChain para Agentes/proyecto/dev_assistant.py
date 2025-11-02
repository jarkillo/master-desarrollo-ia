#!/usr/bin/env python3
"""
Agente de Asistencia al Desarrollo

Combina LangChain (orchestrator) + Agent Skills (workflows complejos)
para asistir en tareas de desarrollo de software.

Funcionalidades:
- 🔍 Code Review usando Agent Skill
- 📁 Búsqueda de código
- ✅ Ejecución de tests
- 💬 Conversación interactiva
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar directorio actual al path para imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

# Importar tools
from tools import SearchCodeTool, TestRunnerTool

console = Console()


def create_dev_agent() -> AgentExecutor:
    """
    Crea el agente de desarrollo con todos los tools.

    Returns:
        AgentExecutor configurado y listo para usar
    """
    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        console.print("[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY no configurada")
        console.print("\n[yellow]Pasos:[/yellow]")
        console.print("1. Copia .env.template a .env")
        console.print("2. Edita .env y agrega tu API key")
        console.print("3. Ejecuta de nuevo")
        sys.exit(1)

    # Configurar LLM
    llm = ChatAnthropic(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022"),
        temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.0")),
        max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))
    )

    # Crear tools
    tools = [
        SearchCodeTool(),
        TestRunnerTool(),
    ]

    # Crear memoria
    memory_type = os.getenv("MEMORY_TYPE", "buffer")

    if memory_type == "buffer":
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    else:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    # Prompt del agente (ReAct pattern)
    react_prompt = PromptTemplate.from_template("""
Eres un asistente de desarrollo de software altamente competente.

Tu objetivo es ayudar al desarrollador con tareas como:
- 🔍 Búsqueda de código en el repositorio
- ✅ Ejecución de tests y análisis de resultados
- 📝 Revisión de código (code review)
- 💡 Sugerencias de mejora

HERRAMIENTAS DISPONIBLES:
{tools}

FORMATO DE RAZONAMIENTO (ReAct):

Thought: [Analiza qué información necesitas y qué herramienta usar]
Action: [Nombre exacto de la herramienta]
Action Input: [Parámetros en formato JSON]
Observation: [Resultado de la herramienta]

... (repite Thought/Action/Observation si necesitas más información)

Thought: Ahora tengo toda la información necesaria para responder
Final Answer: [Tu respuesta final al usuario, en formato Markdown]

INSTRUCCIONES IMPORTANTES:

1. **Usa herramientas cuando sea necesario**: No inventes información que puedes obtener con las tools
2. **Sé específico**: Cuando busques código, usa patrones específicos
3. **Analiza resultados**: No solo retornes el output de las tools, analízalo y da insights
4. **Formato claro**: Usa Markdown para formatear respuestas (listas, código, etc.)
5. **Proactivo**: Si detectas problemas, menciónalos y sugiere soluciones

PREGUNTA DEL USUARIO:
{input}

{agent_scratchpad}
""")

    # Crear agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=react_prompt
    )

    # Executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=os.getenv("AGENT_VERBOSE", "true").lower() == "true",
        max_iterations=10,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )

    return agent_executor


def print_welcome():
    """Muestra mensaje de bienvenida."""
    welcome_text = """
# 🤖 Agente de Asistencia al Desarrollo

Soy tu asistente personal para desarrollo de software.

## 🛠️ Capacidades

- 🔍 **Búsqueda de código** - Encuentra funciones, clases, imports
- ✅ **Ejecución de tests** - Ejecuta pytest y analiza resultados
- 📝 **Code review** - Revisa código siguiendo SOLID y best practices
- 💬 **Conversación** - Recuerdo el contexto de nuestra conversación

## 💡 Ejemplos de Queries

- "Busca todas las funciones que usan SQLAlchemy"
- "Ejecuta los tests en tests/test_api.py"
- "¿Qué archivos contienen la clase BaseModel?"
- "Ejecuta tests con cobertura"

## 📚 Comandos Especiales

- `/help` - Mostrar este mensaje
- `/clear` - Limpiar memoria de conversación
- `/exit` o `/quit` - Salir

---

Escribe tu pregunta o usa un comando.
"""
    console.print(Panel(
        Markdown(welcome_text),
        border_style="cyan",
        title="[bold cyan]Bienvenido[/bold cyan]"
    ))


def interactive_mode(agent: AgentExecutor):
    """
    Modo interactivo del agente.

    Args:
        agent: AgentExecutor configurado
    """
    print_welcome()

    while True:
        try:
            # Obtener input del usuario
            user_input = Prompt.ask("\n[bold cyan]Tú[/bold cyan]")

            # Comandos especiales
            if user_input.lower() in ["/exit", "/quit"]:
                console.print("\n[yellow]👋 ¡Hasta luego![/yellow]\n")
                break

            if user_input.lower() == "/help":
                print_welcome()
                continue

            if user_input.lower() == "/clear":
                agent.memory.clear()
                console.print("[green]✓ Memoria limpiada[/green]")
                continue

            if not user_input.strip():
                continue

            # Ejecutar agente
            console.print("\n[dim]Pensando...[/dim]\n")

            result = agent.invoke({"input": user_input})

            # Mostrar respuesta
            console.print(Panel(
                Markdown(result["output"]),
                title="[bold green]Agente[/bold green]",
                border_style="green"
            ))

        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrumpido. ¡Hasta luego![/yellow]\n")
            break

        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")
            console.print("[dim]El agente continuará funcionando.[/dim]\n")


def single_query_mode(agent: AgentExecutor, query: str):
    """
    Ejecuta una sola query y sale.

    Args:
        agent: AgentExecutor configurado
        query: Pregunta del usuario
    """
    console.print(Panel.fit(
        f"[bold cyan]Query:[/bold cyan] {query}",
        border_style="cyan"
    ))

    try:
        result = agent.invoke({"input": query})

        console.print("\n")
        console.print(Panel(
            Markdown(result["output"]),
            title="[bold green]Respuesta[/bold green]",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        sys.exit(1)


def main():
    """Punto de entrada principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Agente de Asistencia al Desarrollo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Modo interactivo
  python dev_assistant.py

  # Query única
  python dev_assistant.py --query "Busca todas las funciones async"

  # Con verbose desactivado
  python dev_assistant.py --no-verbose
"""
    )

    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Ejecutar una sola query y salir"
    )

    parser.add_argument(
        "--no-verbose",
        action="store_true",
        help="Desactivar modo verbose (no muestra razonamiento)"
    )

    args = parser.parse_args()

    # Override verbose si se especifica
    if args.no_verbose:
        os.environ["AGENT_VERBOSE"] = "false"

    # Crear agente
    console.print("\n[yellow]Inicializando agente...[/yellow]")
    agent = create_dev_agent()
    console.print("[green]✓ Agente listo[/green]\n")

    # Modo de operación
    if args.query:
        single_query_mode(agent, args.query)
    else:
        interactive_mode(agent)


if __name__ == "__main__":
    main()
