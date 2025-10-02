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

Vale, vamos con calma porque este es uno de esos temas que confunde hasta a seniors 😅.


**Merge**

- Une dos ramas creando un nuevo commit especial que mezcla las historias.
- La historia queda con ramas que se cruzan.
- Ventaja: no pierdes nada, todo el historial tal cual pasó.
- Desventaja: el log puede llenarse de “commits de merge” y verse menos lineal.

Ejemplo:

```
A---B---C---D (main)
         \
          E---F (feature)

```

Si haces `git merge feature` en `main`, quedará:

```
A---B---C---D---M (main)
         \     /
          E---F

```

Donde `M` es el commit de merge.

---

**Rebase**

- Coge los commits de tu rama y los “reaplica” como si hubieran nacido encima de otra rama.
- La historia queda limpia y lineal, como si nunca hubiera habido bifurcación.
- Ventaja: un log muy ordenado.
- Desventaja: puede ser peligroso si lo usas en ramas compartidas, porque **reescribe historia**.

Mismo ejemplo inicial:

```
A---B---C---D (main)
         \
          E---F (feature)

```

Si estando en `feature` haces `git rebase main`, quedará:

```
A---B---C---D (main)
              \
               E'---F' (feature)

```

Git reescribió tus commits como nuevos (`E'`, `F'`), ahora la historia parece lineal.

---

### Cuándo usar cada uno

- **Merge**: seguro, colaborativo, perfecto para trabajo en equipo → “quiero juntar estas ramas sin líos”.
- **Rebase**: útil cuando quieres un historial bonito y limpio, por ejemplo antes de abrir un PR, o para tu repo personal.

Regla de oro: **Nunca rebases una rama que otros ya han descargado**, porque a ellos les cambia la historia y se arma un caos.

---

### Aplicación con IA

Un prompt que puedes usar cuando dudes:

```
Rol: Experto en Git.
Tarea: Explícame si en este caso debería usar merge o rebase.
Contexto: Estoy en la rama feature/x, main avanzó con varios commits nuevos, y quiero actualizar mi rama antes de hacer PR.
Formato: Dame los comandos recomendados y explícame por qué.

```

---

## ¿Estás a punto de hacer Merge?

Perfecto, entonces estás en el punto **de decisión real**: tu rama `feature/descripcion-manu` ya contiene tus apuntes en `.md`, pero el PR aún no lo has mergeado.

Aquí tienes dos caminos:

### 1. Haces **Merge directo del PR**

- Lo más seguro y habitual.
- En GitHub: dale a **Merge pull request**.
- Luego en tu PC:
    
    ```bash
    git switch main
    git pull origin main
    git branch -d feature/descripcion-manu   # opcional, para limpiar
    git push origin --delete feature/descripcion-manu  # opcional, limpia en remoto
    
    ```
    
- Con eso tu rama `main` queda con tus apuntes y la rama feature se archiva.

### 2. Cancelas el PR y pruebas **Rebase** para practicar

- Imagina que en `main` alguien hizo commits después de que abriste tu rama (aunque ahora no sea el caso). Podrías rebasear para poner tus commits encima de los últimos.
- Flujo:
    
    ```bash
    git fetch origin
    git switch feature/descripcion-manu
    git rebase origin/main
    git push --force-with-lease
    
    ```
    
- Luego el PR mostraría un historial limpio y lineal.

---

👉 Como es un repo de práctica, mi consejo es:

1. Haz ahora el **Merge normal** en GitHub para que `main` tenga tu trabajo.
2. Luego, crea otra rama (`feature/rebase-test`), haz unos cambios, y allí practicamos rebase contra `main` para que veas cómo queda el historial diferente.

¿Quieres que te prepare un mini-ejercicio de laboratorio con pasos exactos para que compares cómo se ve el `git log` con merge vs con rebase?

