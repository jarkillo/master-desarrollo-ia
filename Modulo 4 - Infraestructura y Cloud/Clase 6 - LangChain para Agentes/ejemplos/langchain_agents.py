#!/usr/bin/env python3
"""
Ejemplos de LangChain Agents - Clase 6

Demuestra:
1. Agent simple con tools básicos
2. ReAct Agent (Reasoning + Acting)
3. Custom Tool creado desde cero
"""

import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

# LangChain imports
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool, StructuredTool
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

# Rich para output
from rich.console import Console
from rich.panel import Panel

console = Console()


# ═══ TOOLS PERSONALIZADOS ═══

def calculator_tool_func(expression: str) -> str:
    """
    Calcula expresión matemática.

    Args:
        expression: Expresión Python (e.g., "2 + 2", "sqrt(16)")

    Returns:
        Resultado del cálculo o mensaje de error
    """
    try:
        # Eval restringido (solo matemáticas básicas)
        import math
        allowed_names = {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "round": round,
            "sum": sum,
            "max": max,
            "min": min
        }

        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Resultado: {result}"

    except Exception as e:
        return f"Error al calcular '{expression}': {str(e)}"


def search_codebase_tool_func(query: str, file_pattern: str = "*.py") -> str:
    """
    Busca código en el repositorio usando grep.

    Args:
        query: Texto a buscar
        file_pattern: Patrón glob para filtrar archivos

    Returns:
        Resultados de la búsqueda (máximo 10 líneas)
    """
    try:
        result = subprocess.run(
            ["grep", "-r", "--include", file_pattern, query, "."],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return f"No se encontró '{query}' en archivos {file_pattern}"

        # Limitar a 10 líneas
        lines = result.stdout.split("\n")[:10]
        output = "\n".join(lines)

        return f"Resultados de búsqueda (máx 10):\n{output}"

    except subprocess.TimeoutExpired:
        return "Error: Búsqueda tardó demasiado (timeout)"
    except Exception as e:
        return f"Error al buscar: {str(e)}"


class SearchCodeInput(BaseModel):
    """Schema de input para search_code tool."""
    query: str = Field(description="Texto a buscar en el código")
    file_pattern: str = Field(
        default="*.py",
        description="Patrón glob (e.g., '*.py', 'api/**/*.py')"
    )


class SearchCodeTool(BaseTool):
    """Custom tool para búsqueda de código."""

    name: str = "search_codebase"
    description: str = """
    Busca código en el repositorio usando grep.

    Útil para:
    - Encontrar definiciones de funciones/clases
    - Buscar imports
    - Encontrar referencias a variables

    Input:
    - query: Texto a buscar
    - file_pattern: Patrón de archivos (default: *.py)

    Ejemplo: search_codebase(query="def calculate_total", file_pattern="api/**/*.py")
    """
    args_schema: type[BaseModel] = SearchCodeInput

    def _run(self, query: str, file_pattern: str = "*.py") -> str:
        """Ejecuta búsqueda."""
        return search_codebase_tool_func(query, file_pattern)


# ═══ EJEMPLOS ═══

def ejemplo_1_agent_basico():
    """Ejemplo 1: Agent con tools básicos"""
    console.print("\n[bold blue]═══ Ejemplo 1: Agent Básico con Tools ═══[/bold blue]\n")

    # LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        max_tokens=2000
    )

    # Definir tools
    calculator_tool = Tool(
        name="calculator",
        func=calculator_tool_func,
        description="""
        Calcula expresiones matemáticas.
        Input: expresión Python válida (e.g., "2 + 2", "sqrt(16)", "10 ** 3")
        Output: Resultado del cálculo
        """
    )

    tools = [calculator_tool]

    # Prompt para ReAct agent
    react_prompt = PromptTemplate.from_template("""
Responde la siguiente pregunta usando las herramientas disponibles si es necesario.

Herramientas disponibles:
{tools}

Usa este formato:

Thought: Razona sobre qué hacer
Action: Nombre de la herramienta a usar (o "Final Answer" si ya tienes la respuesta)
Action Input: Input para la herramienta
Observation: Resultado de la herramienta
... (repite Thought/Action/Observation si es necesario)
Thought: Ahora tengo la respuesta final
Final Answer: La respuesta a la pregunta original

Pregunta: {input}

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
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    # Ejecutar consulta
    query = "¿Cuál es la raíz cuadrada de 256 multiplicada por 3?"

    console.print(f"[yellow]Query:[/yellow] {query}\n")
    console.print("[dim]Ejecutando agent (verbose=True)...[/dim]\n")

    result = agent_executor.invoke({"input": query})

    console.print(Panel(
        result["output"],
        title="[green]Respuesta Final[/green]",
        border_style="green"
    ))


def ejemplo_2_agent_con_custom_tool():
    """Ejemplo 2: Agent con custom tool (búsqueda de código)"""
    console.print("\n[bold blue]═══ Ejemplo 2: Agent con Custom Tool ═══[/bold blue]\n")

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        max_tokens=2000
    )

    # Usar custom tool
    search_code_tool = SearchCodeTool()

    tools = [search_code_tool]

    # Prompt
    react_prompt = PromptTemplate.from_template("""
Eres un asistente de desarrollo de software. Usa las herramientas disponibles para responder preguntas sobre el código.

Herramientas:
{tools}

Formato:

Thought: [tu razonamiento]
Action: [nombre de la herramienta]
Action Input: [input para la herramienta]
Observation: [resultado de la herramienta]
... (repite si es necesario)
Thought: Ahora puedo responder
Final Answer: [respuesta final]

Pregunta: {input}

{agent_scratchpad}
""")

    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    # Consulta
    query = "Busca todas las funciones que comienzan con 'def ejemplo' en archivos Python"

    console.print(f"[yellow]Query:[/yellow] {query}\n")

    result = agent_executor.invoke({"input": query})

    console.print(Panel(
        result["output"],
        title="[green]Respuesta del Agent[/green]",
        border_style="green"
    ))


def ejemplo_3_structured_tool():
    """Ejemplo 3: StructuredTool con múltiples parámetros"""
    console.print("\n[bold blue]═══ Ejemplo 3: StructuredTool ═══[/bold blue]\n")

    def analyze_file(file_path: str, analysis_type: str = "lines") -> str:
        """
        Analiza un archivo del repositorio.

        Args:
            file_path: Ruta al archivo
            analysis_type: Tipo de análisis ("lines", "size", "encoding")

        Returns:
            Resultado del análisis
        """
        from pathlib import Path

        path = Path(file_path)

        if not path.exists():
            return f"Error: Archivo {file_path} no encontrado"

        if analysis_type == "lines":
            try:
                with open(path) as f:
                    lines = f.readlines()
                return f"Archivo {file_path}: {len(lines)} líneas"
            except Exception as e:
                return f"Error al leer {file_path}: {e}"

        elif analysis_type == "size":
            size_bytes = path.stat().st_size
            size_kb = size_bytes / 1024
            return f"Archivo {file_path}: {size_bytes} bytes ({size_kb:.2f} KB)"

        elif analysis_type == "encoding":
            import chardet
            with open(path, 'rb') as f:
                result = chardet.detect(f.read())
            return f"Archivo {file_path}: encoding {result['encoding']} (confidence {result['confidence']:.2f})"

        return f"Tipo de análisis '{analysis_type}' no reconocido"

    # Crear StructuredTool
    analyze_file_tool = StructuredTool.from_function(
        func=analyze_file,
        name="analyze_file",
        description="""
        Analiza archivos del repositorio.

        Parámetros:
        - file_path: Ruta al archivo a analizar
        - analysis_type: "lines" (contar líneas), "size" (tamaño en bytes), "encoding" (detectar encoding)

        Ejemplo: analyze_file(file_path="README.md", analysis_type="lines")
        """
    )

    # Agent
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0,
        max_tokens=1500
    )

    tools = [analyze_file_tool]

    react_prompt = PromptTemplate.from_template("""
Responde usando las herramientas disponibles.

Herramientas: {tools}

Formato:

Thought: [razonamiento]
Action: [herramienta]
Action Input: [parámetros JSON]
Observation: [resultado]
...
Final Answer: [respuesta]

Pregunta: {input}

{agent_scratchpad}
""")

    agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    # Query
    query = "Analiza el archivo README.md: cuántas líneas tiene y cuál es su tamaño"

    console.print(f"[yellow]Query:[/yellow] {query}\n")

    result = agent_executor.invoke({"input": query})

    console.print(Panel(
        result["output"],
        title="[green]Resultado[/green]",
        border_style="green"
    ))


def main():
    """Ejecutar todos los ejemplos."""
    console.print(Panel.fit(
        "[bold cyan]LangChain Agents - Ejemplos Prácticos[/bold cyan]\n"
        "Demostraciones de agents con tools y razonamiento ReAct",
        border_style="cyan"
    ))

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY no configurada")
        return

    try:
        ejemplo_1_agent_basico()
        input("\n[dim]Presiona Enter para continuar...[/dim]\n")

        ejemplo_2_agent_con_custom_tool()
        input("\n[dim]Presiona Enter para continuar...[/dim]\n")

        ejemplo_3_structured_tool()

        console.print("\n[bold green]✓ Todos los ejemplos completados![/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        import traceback
        console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
