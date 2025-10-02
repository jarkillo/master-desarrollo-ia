# Clase 0 - Introducción

Hoy empezamos oficialmente con el **Módulo 0 – Preparación**. Esta semana es como calentar motores: poner orden en tu entorno, tu cabeza y tu forma de hablar con la IA.

Te propongo dividirlo en tres pasos claros:

### 1. Mentalidad de estudio y documentación

Un dev no memoriza todo, sabe **dónde buscar y cómo documentar lo que hace**.

- Vamos a trabajar en **Markdown** y lo ideal es que uses **Notion o un repo en GitHub** para guardar tus apuntes.
- Todo lo que practiquemos lo vas anotando con ejemplos y mini-resúmenes (tipo “esto lo sé, esto no lo entendí, esto lo pido a la IA”).

### 2. Cómo plantear problemas a la IA

No vale tirar preguntas al aire. Queremos prompts estructurados.

Ejemplo simple:

```
Rol: Eres un dev senior experto en bash.
Tarea: Explícame cómo listar todos los procesos que usan más de 50MB de memoria.
Formato: Dame el comando y una breve explicación.

```

Con esa receta, la IA responde más claro y útil.

### 3. Setup del entorno

Hoy quiero que dejes listo:

- **Git** instalado y con tu usuario configurado.
- **IDE (Cursor o VS Code)** funcionando.
- Un repo inicial donde vas a ir subiendo todo lo del máster (ej. `master-ia-manu`).

---

👉 Ejercicio del día:

1. Crea el repo vacío en GitHub y haz tu primer commit con un README.md que diga:
    
    ```
    # Máster Ayla en Desarrollo con IA
    Repo de Manu para el máster
    
    ```
    
2. Sube captura de que el commit quedó hecho.
3. Escríbeme aquí el primer prompt que vayas a usar con la IA esta semana (elige el tema que quieras, puede ser bash, git o Python).

---

### Concepto

Git tiene tres piezas clave:

- **Repositorio local**: lo que tienes en tu máquina.
- **Repositorio remoto** (GitHub): la copia compartida en la nube.
- **Área de preparación (staging)**: lo que marcas como “listo para ser guardado en la historia”.

Con eso, el flujo mínimo es:

`editar archivo → git add → git commit → git push`

Un **Pull Request (PR)** es otra cosa: no es un comando de git, sino una *feature* de GitHub (o GitLab, etc.). Sirve para proponer cambios entre ramas y que alguien (incluido tú) los revise antes de mezclarlos. Es decir:

- Commit: siempre en local (puedes usar terminal o VSCode).
- Push: manda tus commits al remoto.
- Pull Request: se abre en GitHub (o vía CLI de GitHub, pero no desde git puro).

### Aplicación manual (sin IA)

1. Crear repo en GitHub vacío.
2. En tu PC:
    
    ```bash
    git clone <url-del-repo>
    cd <repo>
    echo "# Máster Ayla en Desarrollo con IA" > README.md
    git add README.md
    git commit -m "init: repo del máster"
    git push origin main
    
    ```
    
3. Si luego quieres proponer cambios en otra rama:
    
    ```bash
    git checkout -b feature/readme-update
    # editas archivo
    git add .
    git commit -m "docs: update readme con objetivos"
    git push origin feature/readme-update
    
    ```
    
    Luego entras en GitHub → abres PR de esa rama contra `main`.
    

### Aplicación con IA

Si mañana no recuerdas los comandos, puedes pedirle a la IA algo tipo:

```
Rol: Git coach senior.
Tarea: Estoy en un repo y quiero crear una rama nueva, hacer commit y abrir un PR en GitHub.
Formato: Dame los pasos claros, con comandos de consola.

```

Así la IA te da la receta exacta y tú solo ejecutas.

--- 

¡Eso es! 🎉

Lo hiciste perfecto:

- Hiciste commit en tu rama `feature/descripcion-manu`.
- Hiciste push de la rama al remoto.
- GitHub detectó la rama y te ofreció abrir un Pull Request.
- El PR está abierto, sin conflictos, listo para mergear.

Eso es el flujo moderno de trabajo en equipo:

1. Nadie toca `main` directamente.
2. Cada cambio va en una rama.
3. El cambio se revisa en un PR.
4. Cuando todo está OK → se mergea a `main`.

Aunque estés tú solo, **entrenarte en este hábito es oro puro** porque simula el trabajo en un equipo real.

---

👉 Próximo paso: haz el **merge** del PR desde GitHub y luego en tu máquina ejecuta:

```bash
git checkout main
git pull origin main

```

Con eso tu `main` local se sincroniza con el remoto ya actualizado.

### Explicación de Merge vs Rebase

