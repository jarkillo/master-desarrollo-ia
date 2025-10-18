# Módulo 0: IA Development Foundations

**Duración**: 3 semanas
**Objetivo**: Establecer fundamentos de desarrollo con IA antes de entrar en código avanzado

---

## Visión del Módulo

Este módulo establece el **mindset y herramientas** para trabajar como desarrollador con IA.

**Al terminar, serás capaz de**:
- ✅ Usar Claude Code, Cursor y GitHub Copilot efectivamente
- ✅ Escribir prompts estructurados que generan buen código
- ✅ Crear tus primeros agentes especializados
- ✅ Entender limitaciones de IA y cuándo NO usarla
- ✅ Tener flujo de trabajo: Git + IA + Documentación
- ✅ Criterio para revisar código generado por IA

---

## Estructura del Módulo

### Semana 1: Fundamentos y Herramientas

#### **Clase 1: Fundamentos de IA en Desarrollo** (6h)
**Archivo**: `Clase 1 - Fundamentos de IA en Desarrollo.md`

**Contenido**:
- Qué es y qué NO es IA en desarrollo
- Tipos de herramientas: Copilot, Claude Code, Cursor
- Instalación DESDE CERO:
  - Python 3.12
  - Git
  - Claude Code CLI
  - Cursor IDE (opcional)
- Primer contacto con Claude Code
- Prompt engineering básico
- Proyecto: Generador de contraseñas con IA

**Entregables**:
- Herramientas instaladas y configuradas
- Primer script útil con IA
- Reflexión sobre uso de IA

---

#### **Clase 2: Git + Cursor + Flujo de Trabajo IA** (6h)
**Archivo**: `Clase 2 - Git y Cursor con IA.md`

**Contenido**:
- Git fundamentals (manual implementation)
- Git con IA assistant:
  - Commit messages generados
  - Resolución de conflictos
  - .gitignore automático
- Cursor IDE setup y features
- Conventional Commits
- Proyecto: Repositorio del máster configurado

**Entregables**:
- Repositorio Git configurado
- Primer commit con mensaje de IA
- .cursorrules configurado

---

### Semana 2: Documentación y Agentes

#### **Clase 3: Documentación y Pensamiento Estructurado** (6h)
**Archivo**: `Clase 3 - Documentación y Pensamiento Estructurado.md`

**Contenido**:
- Markdown avanzado
- Diagramas con IA (Mermaid, PlantUML)
- Architecture Decision Records (ADRs)
- Documentación automática
- Proyecto: Documentar TODO el Módulo 0

**Entregables**:
- README profesional
- Diagramas de flujo de trabajo
- ADR: "Por qué uso IA"

---

#### **Clase 4: Tu Primer Agente Custom** (6h)
**Archivo**: `Clase 4 - Tu Primer Agente Custom.md`

**Contenido**:
- Concepto de agentes especializados
- Estructura de `.claude/agents/`
- Diseñar agente Git Commit Helper
- Testing y iteración
- Proyecto: Learning Assistant personalizado

**Entregables**:
- Agente Git Commit Helper
- Agente Learning Assistant
- Documentación de uso

---

### Semana 3: Avanzado y Ética

#### **Clase 5: Prompt Engineering Avanzado** (6h)
**Archivo**: `Clase 5 - Prompt Engineering Avanzado.md`

**Contenido**:
- Patrones avanzados:
  - Few-shot learning
  - Chain of thought
  - Role prompting
- Context management
- Biblioteca de prompts
- Proyecto: Prompt Library personal (50+ prompts)

**Entregables**:
- Prompt Library documentada
- Mini-proyecto usando prompts

---

#### **Clase 6: Limitaciones y Ética** (6h)
**Archivo**: `Clase 6 - Limitaciones y Ética.md`

**Contenido**:
- Cuándo NO usar IA
- Failure modes (hallucinations, código desactualizado)
- Seguridad y ética
- Auditar código generado por IA
- Proyecto: "Mi contrato con la IA"

**Entregables**:
- AI Usage Policy personal
- Auditoría de código del módulo
- Re-implementación manual de lo no entendido

---

## Mini-Proyecto Final del Módulo

### CLI de Tareas con IA (Preparación para Módulo 1)

**Objetivo**: Crear versión simple de CLI de tareas usando todo lo aprendido.

**Requisitos**:
1. **Diseño** (TÚ):
   - Qué features tendrá
   - Qué arquitectura (funciones, flujo)
2. **Implementación** (TÚ + IA):
   - Usar prompts de tu biblioteca
   - Generar código función por función
   - Revisar cada línea
3. **Testing** (TÚ + IA):
   - Tests generados pero TÚ los entiendes
4. **Documentación** (TÚ + IA):
   - README profesional
   - Diagramas Mermaid
5. **Git** (TÚ + IA):
   - Commits con conventional commits
   - Agente Git Commit Helper
6. **Agente** (TÚ):
   - Crear "CLI Reviewer" que valida tu CLI

**Entregables**:
- Código funcionando
- Tests >80% coverage
- Documentación completa
- Agente CLI Reviewer
- Reflexión: "Qué hizo IA vs qué hice yo"

**Tiempo**: 1 semana

---

## Instalación Requerida

Antes de empezar Clase 1, asegúrate de tener:

### Hardware Mínimo
- 💻 Computadora con 8GB RAM (16GB recomendado)
- 📦 20GB espacio en disco
- 🌐 Conexión a Internet estable

### Software a Instalar (se enseña en Clase 1)
- [ ] Python 3.12+
- [ ] Git
- [ ] Claude Code CLI
- [ ] Editor de código (VS Code o Cursor)

### Cuentas Requeridas
- [ ] GitHub account (gratis)
- [ ] Anthropic account (para Claude API)
- [ ] (Opcional) GitHub Copilot subscription

---

## Filosofía del Módulo

### 🎯 Objetivo No Es:
- ❌ "IA hace todo por ti"
- ❌ "No necesitas aprender fundamentos"
- ❌ "Copia código sin entender"

### ✅ Objetivo SÍ Es:
- ✅ "IA te hace 3-5x más productivo"
- ✅ "Aprendes fundamentos profundamente, IA acelera práctica"
- ✅ "Entiendes TODO el código que usas"

### Regla de Oro

**60% TÚ / 40% IA**
- TÚ diseñas, decides, entiendes
- IA genera, acelera, sugiere
- TÚ revisas, validas, aprendes

---

## Evaluación del Módulo

### Criterios (100 puntos)

**Comprensión de IA** (30 puntos):
- Entiendes qué es y qué no es IA
- Sabes cuándo usar y NO usar
- Identificas limitaciones

**Habilidades Técnicas** (40 puntos):
- Prompts bien estructurados
- Agentes funcionando
- Git + IA workflow establecido
- Código generado funciona

**Criterio y Reflexión** (30 puntos):
- Revisas código críticamente
- Entiendes lo que IA genera
- Reflexiones demuestran aprendizaje
- Auditas tus propias decisiones

### Proyecto Final (40% de la nota)

Mini-proyecto CLI debe demostrar:
- ✅ Diseño propio claro
- ✅ Uso efectivo de IA (prompts, agentes)
- ✅ Código que TÚ entiendes
- ✅ Documentación profesional
- ✅ Reflexión profunda

---

## Recursos del Módulo

### Documentación Oficial
- [Claude Code Docs](https://docs.anthropic.com/claude/docs/)
- [Git Book](https://git-scm.com/book/en/v2)
- [Cursor Docs](https://cursor.sh/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai)

### Plantillas Incluidas
```
.templates/
├── prompt-template.md          # Plantilla de prompts
├── agent-template.md           # Plantilla de agentes
├── adr-template.md             # Architecture Decision Record
└── reflection-template.md      # Reflexión de clase
```

### Agent Library Inicial
```
.claude/agents/educational/
├── git-commit-helper.md
├── learning-assistant.md
└── code-reviewer-basic.md
```

---

## Progresión de Aprendizaje

### Semana 1: IA Novice
```
Estado: "Primer contacto con IA"
Puedes:
- Hacer preguntas a Claude Code
- Generar código simple
- Entender respuestas de IA

No puedes aún:
- Diseñar agentes
- Prompts complejos
- Auditar código crítico
```

### Semana 2: IA Assistant User
```
Estado: "Uso básico de herramientas"
Puedes:
- Usar Git con IA
- Crear agentes simples
- Documentar con IA
- Iteración de prompts

No puedes aún:
- Orquestar múltiples agentes
- Prompt engineering avanzado
```

### Semana 3: IA Foundations Complete
```
Estado: "Bases sólidas establecidas"
Puedes:
- Usar IA efectivamente en desarrollo
- Crear agentes útiles
- Prompts estructurados
- Criterio para revisar IA
- Workflow Git + IA establecido

Listo para: Módulo 1 (Fundamentos + IA Assistant)
```

---

## Troubleshooting Común

### Instalación de Claude Code

**Error**: `ANTHROPIC_API_KEY not found`
```bash
# Verificar variable de entorno
# Windows:
echo %ANTHROPIC_API_KEY%

# macOS/Linux:
echo $ANTHROPIC_API_KEY

# Si no aparece, revisar Clase 1 sección 2.3
```

### Git Issues

**Error**: `fatal: not a git repository`
```bash
# Inicializar repo:
git init
```

### Python Path Issues

**Error**: `python: command not found`
```bash
# Windows: Reinstalar Python marcando "Add to PATH"
# macOS/Linux: Usar python3 en vez de python
```

---

## Siguiente Módulo

**Módulo 1: Fundamentos + IA Assistant**

Prepárate para:
- Python fundamentals profundos
- CLI apps con IA assistance
- Testing con TDD + IA
- Clean Code revisado por agentes

**Prerequisitos para Módulo 1**:
- ✅ Módulo 0 completado
- ✅ Herramientas instaladas
- ✅ Al menos 2 agentes creados
- ✅ Biblioteca de prompts iniciada
- ✅ Mini-proyecto CLI funcionando

---

## Notas Finales

**Mentalidad correcta para el máster**:

1. **Fundamentos primero, IA después** - Aprende manualmente, luego acelera con IA
2. **Entender > Copiar** - Si no entiendes, no uses
3. **IA es copiloto, no piloto** - TÚ diriges
4. **Itera siempre** - Prompts mejoran con práctica
5. **Comparte aprendizajes** - Agentes útiles, documenta

**Recuerda la visión**:
> "Un desarrollador solo con un ejército de agentes"

Estás construyendo ese ejército. El Módulo 0 son los fundamentos.

¡Adelante! 🚀
