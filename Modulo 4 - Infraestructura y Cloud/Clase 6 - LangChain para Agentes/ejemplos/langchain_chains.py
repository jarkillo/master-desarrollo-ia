#!/usr/bin/env python3
"""
Ejemplos de LangChain Chains - Clase 6

Demuestra:
1. Simple Chain (prompt → LLM → output)
2. Sequential Chain (múltiples pasos encadenados)
3. Custom Chain con output parsing
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones de LangChain
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import LLMChain, SequentialChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# Rich para output bonito
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def ejemplo_1_simple_chain():
    """Ejemplo 1: Chain simple (Prompt → LLM → Output)"""
    console.print("\n[bold blue]═══ Ejemplo 1: Simple Chain ═══[/bold blue]\n")

    # 1. Definir LLM
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        max_tokens=1000
    )

    # 2. Definir prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente experto en {topic}. Responde de forma concisa."),
        ("user", "{question}")
    ])

    # 3. Crear chain: prompt | llm | parser
    chain = prompt | llm | StrOutputParser()

    # 4. Ejecutar
    question = "¿Cómo funciona el GIL (Global Interpreter Lock)?"
    console.print(f"[yellow]Pregunta:[/yellow] {question}")
    console.print("[yellow]Topic:[/yellow] Python\n")

    result = chain.invoke({
        "topic": "Python",
        "question": question
    })

    console.print(Panel(
        Markdown(result),
        title="[green]Respuesta del LLM[/green]",
        border_style="green"
    ))


def ejemplo_2_sequential_chain():
    """Ejemplo 2: Sequential Chain (múltiples pasos)"""
    console.print("\n[bold blue]═══ Ejemplo 2: Sequential Chain ═══[/bold blue]\n")

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.7,
        max_tokens=500
    )

    # Chain 1: Generar outline
    outline_prompt = PromptTemplate.from_template(
        "Genera un outline de 3 puntos para un artículo sobre: {topic}"
    )
    outline_chain = LLMChain(
        llm=llm,
        prompt=outline_prompt,
        output_key="outline"
    )

    # Chain 2: Escribir introducción basada en outline
    intro_prompt = PromptTemplate.from_template(
        """
        Outline del artículo:
        {outline}

        Escribe una introducción compelling de 2 párrafos para este artículo.
        """
    )
    intro_chain = LLMChain(
        llm=llm,
        prompt=intro_prompt,
        output_key="introduction"
    )

    # Chain 3: Escribir conclusión
    conclusion_prompt = PromptTemplate.from_template(
        """
        Outline: {outline}
        Introducción: {introduction}

        Escribe una conclusión de 1 párrafo que conecte los puntos principales.
        """
    )
    conclusion_chain = LLMChain(
        llm=llm,
        prompt=conclusion_prompt,
        output_key="conclusion"
    )

    # Encadenar todo
    full_chain = SequentialChain(
        chains=[outline_chain, intro_chain, conclusion_chain],
        input_variables=["topic"],
        output_variables=["outline", "introduction", "conclusion"],
        verbose=True
    )

    # Ejecutar
    topic = "Agent Skills vs LangChain"
    console.print(f"[yellow]Topic:[/yellow] {topic}\n")

    result = full_chain({"topic": topic})

    # Mostrar resultados
    console.print(Panel(
        result["outline"],
        title="[cyan]1. Outline[/cyan]",
        border_style="cyan"
    ))

    console.print(Panel(
        Markdown(result["introduction"]),
        title="[green]2. Introducción[/green]",
        border_style="green"
    ))

    console.print(Panel(
        Markdown(result["conclusion"]),
        title="[magenta]3. Conclusión[/magenta]",
        border_style="magenta"
    ))


def ejemplo_3_custom_output_parser():
    """Ejemplo 3: Chain con Pydantic Output Parser"""
    console.print("\n[bold blue]═══ Ejemplo 3: Chain con Output Parsing ═══[/bold blue]\n")

    # 1. Definir schema de output con Pydantic
    class TechnicalConcept(BaseModel):
        """Schema para concepto técnico explicado."""
        nombre: str = Field(description="Nombre del concepto")
        definicion: str = Field(description="Definición en 1-2 frases")
        analogia: str = Field(description="Analogía simple para entenderlo")
        ejemplo_codigo: str = Field(description="Ejemplo de código comentado")
        cuando_usar: str = Field(description="Cuándo usar este concepto")
        cuando_no_usar: str = Field(description="Cuándo NO usar este concepto")

    # 2. Crear parser
    parser = PydanticOutputParser(pydantic_object=TechnicalConcept)

    # 3. Crear prompt con instrucciones de formato
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.3,  # Baja temperatura para output estructurado
        max_tokens=1500
    )

    prompt = PromptTemplate.from_template(
        """
        Explica el siguiente concepto técnico de forma estructurada.

        Concepto: {concepto}

        {format_instructions}
        """,
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # 4. Chain
    chain = prompt | llm | parser

    # 5. Ejecutar
    concepto = "Dependency Injection"
    console.print(f"[yellow]Concepto a explicar:[/yellow] {concepto}\n")

    result: TechnicalConcept = chain.invoke({"concepto": concepto})

    # Mostrar resultado estructurado
    console.print(Panel(
        f"""[bold]{result.nombre}[/bold]

[yellow]Definición:[/yellow]
{result.definicion}

[yellow]Analogía:[/yellow]
{result.analogia}

[yellow]Ejemplo de Código:[/yellow]
```python
{result.ejemplo_codigo}
```

[yellow]✅ Cuándo Usar:[/yellow]
{result.cuando_usar}

[yellow]❌ Cuándo NO Usar:[/yellow]
{result.cuando_no_usar}
""",
        title="[green]Concepto Explicado (Structured Output)[/green]",
        border_style="green"
    ))


def main():
    """Ejecutar todos los ejemplos."""
    console.print(Panel.fit(
        "[bold cyan]LangChain Chains - Ejemplos Prácticos[/bold cyan]\n"
        "Demostraciones de diferentes tipos de chains",
        border_style="cyan"
    ))

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY no configurada")
        console.print("Crea un archivo .env con:")
        console.print("  ANTHROPIC_API_KEY=tu_api_key_aqui")
        return

    try:
        # Ejecutar ejemplos
        ejemplo_1_simple_chain()
        input("\n[dim]Presiona Enter para continuar...[/dim]\n")

        ejemplo_2_sequential_chain()
        input("\n[dim]Presiona Enter para continuar...[/dim]\n")

        ejemplo_3_custom_output_parser()

        console.print("\n[bold green]✓ Todos los ejemplos completados![/bold green]\n")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        import traceback
        console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
