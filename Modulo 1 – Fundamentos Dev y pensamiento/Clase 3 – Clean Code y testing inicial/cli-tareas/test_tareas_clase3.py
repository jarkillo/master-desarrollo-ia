# test_tareas.py

# ================================
# 0. IMPORTAR LIBRERIAS
# ================================

import os
import tempfile
import unittest

from tareas import (
    agregar_tarea,
    cargar_tareas,
    completar_tarea,
    guardar_tareas,
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

    def test_agregar_tarea(self):
        agregar_tarea(self.tmp, "Estudiar IA")
        tareas = cargar_tareas(self.tmp)
        self.assertEqual(len(tareas), 1)
        self.assertEqual(tareas[0]["nombre"], "Estudiar IA")
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


# ================================
# 2. MAIN
# ================================

if __name__ == "__main__":
    unittest.main()
