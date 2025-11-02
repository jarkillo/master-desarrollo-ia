#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) Básico - Clase 6

Demuestra:
1. Cargar documentos y crear chunks
2. Crear vector store con FAISS
3. Implementar QA chain con RAG
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def ejemplo_rag_completo():
    """Ejemplo completo de RAG: indexar docs → buscar → generar respuesta"""
    console.print(Panel.fit(
        "[bold cyan]RAG (Retrieval-Augmented Generation)[/bold cyan]\n"
        "Sistema de Q&A sobre documentos locales",
        border_style="cyan"
    ))

    # PASO 1: Crear documentos de ejemplo si no existen
    docs_dir = Path("docs_ejemplo")
    docs_dir.mkdir(exist_ok=True)

    # Documentos de ejemplo sobre Agent Skills y LangChain
    docs_content = {
        "agent_skills.md": """
# Agent Skills

Agent Skills son paquetes modulares de conocimiento que extienden las capacidades de Claude.

## Características

- **Progressive Disclosure**: Carga información por capas
- **Filesystem-based**: Organizados en carpetas
- **Escalable**: Puede tener 100+ skills sin saturar context window

## Componentes

Un Agent Skill consiste en:
1. SKILL.md - Descripción y workflow
2. Archivos de soporte - Referencias, ejemplos
3. Scripts Python (opcional) - Código ejecutable
""",
        "langchain.md": """
# LangChain

LangChain es un framework para construir aplicaciones con LLMs mediante composición de componentes.

## Componentes Principales

- **Chains**: Secuencias de transformaciones
- **Agents**: Entidades que razonan y usan tools
- **Memory**: Persistencia de contexto
- **Tools**: Funciones que el agent puede invocar

## Uso

```python
from langchain.chains import ConversationChain
chain = ConversationChain(llm=llm, memory=memory)
```
""",
        "comparacion.md": """
# Agent Skills vs LangChain

## Agent Skills
- **Fortaleza**: Workflows complejos con conocimiento procedimental
- **Formato**: Markdown + scripts
- **Escalabilidad**: Ilimitada (progressive disclosure)

## LangChain
- **Fortaleza**: Orchestración de tools y multi-LLM
- **Formato**: Código Python
- **Testing**: Fácil (unit tests estándar)

## Recomendación
Usa ambos de forma híbrida: LangChain como orchestrator + Agent Skills para workflows complejos.
"""
    }

    for filename, content in docs_content.items():
        (docs_dir / filename).write_text(content)

    console.print(f"[green]✓[/green] Documentos creados en {docs_dir}/\n")

    # PASO 2: Cargar documentos
    console.print("[yellow]Cargando documentos...[/yellow]")

    loader = DirectoryLoader(
        str(docs_dir),
        glob="**/*.md",
        loader_cls=TextLoader
    )
    documents = loader.load()

    console.print(f"[green]✓[/green] Cargados {len(documents)} documentos\n")

    # PASO 3: Dividir en chunks
    console.print("[yellow]Dividiendo en chunks...[/yellow]")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    console.print(f"[green]✓[/green] Creados {len(chunks)} chunks\n")

    # PASO 4: Crear embeddings y vector store
    console.print("[yellow]Creando vector store (esto puede tardar)...[/yellow]")

    # Usar embeddings open-source (HuggingFace) en lugar de OpenAI
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    console.print(f"[green]✓[/green] Vector store creado con {vectorstore.index.ntotal} vectores\n")

    # PASO 5: Crear retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Top 3 chunks más relevantes
    )

    # PASO 6: Crear QA chain
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        temperature=0.3,
        max_tokens=1000
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Meter todos los docs en el prompt
        retriever=retriever,
        return_source_documents=True
    )

    console.print("[green]✓[/green] Sistema RAG listo\n")

    # PASO 7: Hacer preguntas
    questions = [
        "¿Qué son los Agent Skills?",
        "¿Cuáles son los componentes principales de LangChain?",
        "¿Cuándo debo usar Agent Skills vs LangChain?"
    ]

    for i, question in enumerate(questions, 1):
        console.print(f"\n[bold cyan]Pregunta {i}:[/bold cyan] {question}\n")

        result = qa_chain({"query": question})

        # Respuesta
        console.print(Panel(
            Markdown(result["result"]),
            title="[green]Respuesta (Generada con RAG)[/green]",
            border_style="green"
        ))

        # Fuentes
        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        console.print("\n[dim]📚 Fuentes consultadas:[/dim]")
        for src in set(sources):
            console.print(f"  - {Path(src).name}")

        if i < len(questions):
            input("\n[dim]Presiona Enter para siguiente pregunta...[/dim]\n")

    console.print("\n[bold green]✓ Demo de RAG completada![/bold green]\n")


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[bold red]ERROR:[/bold red] ANTHROPIC_API_KEY no configurada")
        return

    try:
        ejemplo_rag_completo()

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        import traceback
        console.print(traceback.format_exc())


if __name__ == "__main__":
    main()
