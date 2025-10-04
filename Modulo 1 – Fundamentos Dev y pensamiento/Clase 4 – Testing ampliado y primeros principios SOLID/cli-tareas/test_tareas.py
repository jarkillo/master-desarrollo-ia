# test_tareas.py

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

import os, tempfile, unittest
from tareas import (
    guardar_tareas,
    cargar_tareas,
    agregar_tarea,
    completar_tarea,
    listar_tareas,
)


# ================================
# 1. CLASE DE PRUEBAS
# ================================


class TestTareas(unittest.TestCase):

    def setUp(self):
        fd, self.tmp = tempfile.mkstemp(prefix="tareas_", suffix=".json")
        os.close(fd)
        guardar_tareas(self.tmp, [])

    def tearDown(self):
        os.remove(self.tmp)

    def test_agregar_tarea_con_prioridad(self):
        tarea = agregar_tarea(self.tmp, "Estudiar IA", "alta")
        tareas = cargar_tareas(self.tmp)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertEqual(tareas[0]["prioridad"], "alta")
        self.assertFalse(tareas[0]["completada"])

    def test_completar_tarea(self):
        tarea = agregar_tarea(self.tmp, "Repasar Git")
        ok = completar_tarea(self.tmp, tarea["id"])
        self.assertTrue(ok)
        tareas = listar_tareas(self.tmp)
        self.assertTrue(tareas[0]["completada"])

    def test_completar_inexistente(self):
        guardar_tareas(self.tmp, [])
        ok = completar_tarea(self.tmp, 999)
        self.assertFalse(ok)

    def test_listar_vacio(self):
        # Arrancamos con el archivo vacío
        guardar_tareas(self.tmp, [])

        tareas = listar_tareas(self.tmp)

        # La lista debe estar vacía
        self.assertEqual(tareas, [])

    def test_listar_con_tareas(self):
        # Agrego dos tareas
        agregar_tarea(self.tmp, "Estudiar IA")
        agregar_tarea(self.tmp, "Repasar Git")

        tareas = listar_tareas(self.tmp)

        # Debe haber 2 tareas
        self.assertEqual(len(tareas), 2)

        # Verificamos que los nombres están correctos
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
        self.assertEqual(tareas[1]["nombre"], "Repasar Git")

        # Ambas deben empezar como no completadas
        self.assertFalse(tareas[0]["completada"])
        self.assertFalse(tareas[1]["completada"])

    def test_agregar_tarea_prioridad_por_defecto(self):
        nueva = agregar_tarea(self.tmp, "Repasar SOLID")  # sin prioridad
        self.assertEqual(nueva["prioridad"], "media")

    def test_agregar_tarea_con_prioridad_alta(self):
        nueva = agregar_tarea(self.tmp, "Estudiar IA", "alta")
        self.assertEqual(nueva["prioridad"], "alta")

    def test_listar_solo_prioridad_alta(self):
        agregar_tarea(self.tmp, "Estudiar IA", "alta")
        agregar_tarea(self.tmp, "Repasar Git", "baja")
        agregar_tarea(self.tmp, "Llamar a mamá", "media")

        tareas_alta = listar_tareas(self.tmp, prioridad="alta")

        # Debe haber exactamente 1 tarea
        self.assertEqual(len(tareas_alta), 1)

        # Esa tarea debe ser la de "Estudiar IA"
        self.assertEqual(tareas_alta[0]["nombre"], "Estudiar IA")
        self.assertEqual(tareas_alta[0]["prioridad"], "alta")


# ================================
# 2. MAIN
# ================================

if __name__ == "__main__":
    unittest.main()
