import sys

# Código "feo" pero funcional
# Problemas:
# 1. Todo en el nivel principal (no hay funciones)
# 2. Lógica de validación repetida
# 3. Mensajes mezclados con lógica
# 4. Imposible testear sin ejecutar el script completo

if len(sys.argv) < 2:
    print("Uso: python tareas.py <comando>")
else:
    comando = sys.argv[1]

    if comando == "listar":
        print("=== LISTA DE TAREAS ===")
        print("[ ] 1. Estudiar Git")
        print("[ ] 2. Hacer ejercicio")
        print("[x] 3. Leer documentación")

    elif comando == "agregar":
        if len(sys.argv) < 3:
            print("Error: falta el texto de la tarea")
        else:
            tarea = sys.argv[2]
            print(f"Tarea agregada: {tarea}")
            print("Total de tareas: 4")

    elif comando == "completar":
        if len(sys.argv) < 3:
            print("Error: falta el ID")
        else:
            task_id = sys.argv[2]
            print(f"Tarea {task_id} marcada como completada")
            print("¡Buen trabajo!")

    else:
        print("Comando no reconocido")


# EJERCICIO:
# Refactoriza este código siguiendo estos pasos:
# 1. Extrae función mostrar_uso()
# 2. Extrae funciones comando_listar(), comando_agregar(tarea), comando_completar(task_id)
# 3. Crea función main() que orqueste todo
# 4. Añade if __name__ == "__main__": main()
