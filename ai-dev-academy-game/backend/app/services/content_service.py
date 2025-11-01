"""Content service - Manages curriculum structure and content."""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ClassInfo:
    """Information about a class."""
    class_number: int
    title: str
    description: str
    exercises_count: int
    xp_reward: int
    prerequisite: Optional[int] = None  # Previous class number (None for first class)


@dataclass
class ModuleInfo:
    """Information about a module."""
    module_number: int
    title: str
    description: str
    classes: List[ClassInfo]


# Curriculum structure based on master-ia-manu repository
CURRICULUM: Dict[int, ModuleInfo] = {
    0: ModuleInfo(
        module_number=0,
        title="IA Development Foundations",
        description="AI tools setup, prompt engineering, first agents, Git + IA workflow",
        classes=[
            ClassInfo(0, "Intro al Desarrollo con IA", "Introducción al desarrollo asistido por IA", 3, 100),
            ClassInfo(1, "Setup de Herramientas IA", "Configuración de herramientas", 5, 150),
            ClassInfo(2, "Primeros Agentes", "Crear tus primeros agentes de IA", 4, 200),
            ClassInfo(3, "Git + IA Workflow", "Flujo de trabajo con Git y IA", 6, 250),
            ClassInfo(4, "Prompt Engineering Básico", "Fundamentos de prompt engineering", 8, 300),
            ClassInfo(5, "Context Engineering", "Gestión de contexto en IA", 7, 350),
        ]
    ),
    1: ModuleInfo(
        module_number=1,
        title="Fundamentos + IA Assistant",
        description="CLI applications, Python basics, testing with AI assistance",
        classes=[
            ClassInfo(0, "Python Básico con IA", "Fundamentos de Python asistido", 10, 200),
            ClassInfo(1, "CLI Applications", "Aplicaciones de línea de comandos", 8, 250),
            ClassInfo(2, "Testing con IA", "Test-Driven Development con IA", 12, 300),
            ClassInfo(3, "Debugging con IA", "Depuración asistida por IA", 10, 350),
        ]
    ),
    2: ModuleInfo(
        module_number=2,
        title="Arquitectura + Agent Orchestration",
        description="FastAPI, SOLID, clean architecture, specialized agent teams",
        classes=[
            ClassInfo(0, "Intro a FastAPI", "Primeros pasos con FastAPI", 8, 300),
            ClassInfo(1, "SOLID Principles", "Principios SOLID con ejemplos", 10, 350),
            ClassInfo(2, "Clean Architecture", "Arquitectura limpia en Python", 12, 400),
            ClassInfo(3, "Dependency Injection", "Inversión de dependencias", 10, 450),
            ClassInfo(4, "Open/Closed Principle", "Principio abierto/cerrado", 8, 400),
            ClassInfo(5, "Integration Testing", "Pruebas de integración", 14, 500),
            ClassInfo(6, "CI/CD con IA", "Integración continua con IA", 12, 550),
        ]
    ),
    3: ModuleInfo(
        module_number=3,
        title="Seguridad + IA con Criterio",
        description="Security hardening, JWT, auditing AI-generated code",
        classes=[
            ClassInfo(0, "Código que se defiende", "Seguridad defensiva en código", 10, 400),
            ClassInfo(1, "Seguridad Básica en APIs", "Fundamentos de seguridad", 12, 450),
            ClassInfo(2, "Auditoría con IA", "Auditoría de código con IA", 10, 500),
            ClassInfo(3, "JWT Authentication", "Autenticación con JWT", 14, 550),
            ClassInfo(4, "Seguridad Avanzada", "Técnicas avanzadas de seguridad", 12, 600),
            ClassInfo(5, "Defensa Activa", "Defensa activa y pipelines", 10, 550),
            ClassInfo(6, "CICD Inteligente", "CI/CD con validación IA", 14, 650),
            ClassInfo(7, "Observability con Sentry", "Observabilidad y alertas", 12, 600),
        ]
    ),
    4: ModuleInfo(
        module_number=4,
        title="Infrastructure + AI DevOps",
        description="Docker, databases, cloud deployment with AI agents",
        classes=[
            ClassInfo(0, "Del Código Local al Cloud", "Introducción a deployment", 8, 500),
            ClassInfo(1, "API en Contenedor", "Containerización con Docker", 10, 550),
            ClassInfo(2, "Base de Datos SQLAlchemy", "ORM y bases de datos", 14, 600),
            ClassInfo(3, "Migraciones con Alembic", "Gestión de migraciones", 12, 650),
            ClassInfo(4, "Deploy a Railway", "Deployment en Railway", 10, 600),
            ClassInfo(5, "LangChain para Agentes", "Orquestación con LangChain", 16, 700),
            ClassInfo(6, "Claude Agent SDK", "Building Agents con Claude", 14, 750),
            ClassInfo(7, "Writing Tools for AI", "Crear herramientas para IA", 12, 700),
            ClassInfo(8, "AI DevOps Automation", "Automatización DevOps con IA", 16, 800),
        ]
    ),
    5: ModuleInfo(
        module_number=5,
        title="Full-Stack + Agent Mastery",
        description="Complete projects with orchestrated agent teams",
        classes=[
            ClassInfo(0, "React + FastAPI Integration", "Full-stack con React", 18, 800),
            ClassInfo(1, "State Management", "Gestión de estado avanzada", 16, 850),
            ClassInfo(2, "Auth Full-Stack", "Autenticación completa", 14, 900),
            ClassInfo(3, "Deploy Full-Stack", "Deployment de aplicaciones completas", 12, 850),
            ClassInfo(4, "Agent Orchestration Mastery", "Orquestación avanzada de agentes", 20, 1000),
        ]
    )
}


def get_module_info(module_number: int) -> Optional[ModuleInfo]:
    """Get information about a specific module."""
    return CURRICULUM.get(module_number)


def get_class_info(module_number: int, class_number: int) -> Optional[ClassInfo]:
    """Get information about a specific class."""
    module = CURRICULUM.get(module_number)
    if not module:
        return None

    for class_info in module.classes:
        if class_info.class_number == class_number:
            return class_info

    return None


def get_all_modules() -> List[ModuleInfo]:
    """Get all modules in curriculum order."""
    return [CURRICULUM[i] for i in sorted(CURRICULUM.keys())]


def get_total_classes() -> int:
    """Get total number of classes across all modules."""
    return sum(len(module.classes) for module in CURRICULUM.values())


def get_total_xp() -> int:
    """Get total XP available across all classes."""
    total = 0
    for module in CURRICULUM.values():
        for class_info in module.classes:
            total += class_info.xp_reward
    return total


def is_class_unlockable(
    module_number: int,
    class_number: int,
    completed_classes: List[tuple]  # List of (module_number, class_number) tuples
) -> bool:
    """
    Check if a class can be unlocked based on prerequisites.

    Rules:
    - Module 0 Class 0: Always unlockable (starting point)
    - Other classes in same module: Previous class must be completed
    - First class of new module: All classes in previous module must be completed
    """
    # Module 0 Class 0 is always unlockable
    if module_number == 0 and class_number == 0:
        return True

    class_info = get_class_info(module_number, class_number)
    if not class_info:
        return False

    # Check if previous class in same module is completed
    if class_number > 0:
        prev_class = (module_number, class_number - 1)
        return prev_class in completed_classes

    # First class of a new module (class_number == 0, module_number > 0)
    # Requires all classes of previous module to be completed
    if module_number > 0:
        prev_module = CURRICULUM.get(module_number - 1)
        if not prev_module:
            return False

        # Check all classes in previous module are completed
        for prev_class_info in prev_module.classes:
            if (module_number - 1, prev_class_info.class_number) not in completed_classes:
                return False

        return True

    return False


def get_next_unlockable_class(
    completed_classes: List[tuple]
) -> Optional[tuple]:
    """
    Get the next class that can be unlocked.

    Returns (module_number, class_number) or None if curriculum is complete.
    """
    for module_number in sorted(CURRICULUM.keys()):
        module = CURRICULUM[module_number]
        for class_info in module.classes:
            class_tuple = (module_number, class_info.class_number)
            # Skip if already completed
            if class_tuple in completed_classes:
                continue
            # Check if unlockable
            if is_class_unlockable(module_number, class_info.class_number, completed_classes):
                return class_tuple

    return None  # Curriculum complete!


def calculate_progress_percentage(completed_classes: int, total_classes: int) -> float:
    """Calculate progress percentage."""
    if total_classes == 0:
        return 0.0
    return round((completed_classes / total_classes) * 100, 2)


def get_module_progress(
    module_number: int,
    completed_classes_in_module: int
) -> float:
    """Calculate progress percentage for a specific module."""
    module = CURRICULUM.get(module_number)
    if not module:
        return 0.0

    total_classes = len(module.classes)
    return calculate_progress_percentage(completed_classes_in_module, total_classes)
