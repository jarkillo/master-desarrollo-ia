import sys  # sys nos da acceso a los argumentos de la terminal

# Si el usuario no puso nada más después de "python tareas.py"
# Si hay menos de dos argumentos (El primero es el nombre del programa):
if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>")  # Imprimimos en pantalla el mensaje

# En caso contrario:
else:
    # Creamos la variable comando y metemos dentro el argumento.
    comando = sys.argv[1]  # el segundo argumento: listar, agregar, etc.

    # Ojo, es sys.argv[1] porque en python empezamos desde el 0, es decir,
    # el primer argumento sería el [0] = tareas.py
    # el segundo argumento sería el [1] = listar / agregar / completar

    # Si el comando es listar
    if comando == "listar":
        print("Aquí se mostrarían las tareas")  # Imprimimos el mensaje

    # Si es agregar
    elif comando == "agregar":
        print("Aquí se agregaría una tarea")  # Imprimimos el mensaje

    # si es completar
    elif comando == "completar":
        print("Aquí se completaría una tarea")  # Imprimimos el mensaje

    else:
        print("Comando no reconocido")  # Avisamos del error
