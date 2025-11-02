"""Tests de integración para validar que todos los repositorios son intercambiables.

Estos tests validan que RepositorioMemoria y RepositorioJSON cumplen
exactamente el mismo contrato (RepositorioTareas Protocol).

Si algún test falla solo para un repositorio, significa que NO son
intercambiables → violación de Liskov Substitution Principle.
"""

import pytest
from api.repositorio_json import RepositorioJSON
from api.repositorio_memoria import RepositorioMemoria
from api.servicio_tareas import Tarea


@pytest.fixture(params=["memoria", "json"])
def repositorio(request, tmp_path):
    """Fixture parametrizado que devuelve cada repositorio.

    Args:
        request: Objeto de pytest con parámetro actual
        tmp_path: Directorio temporal provisto por pytest

    Yields:
        RepositorioMemoria o RepositorioJSON (cada test corre 2 veces)

    Nota:
        Usa tmp_path para RepositorioJSON para evitar conflictos entre tests.
    """
    if request.param == "memoria":
        yield RepositorioMemoria()
    elif request.param == "json":
        archivo_test = tmp_path / f"tareas_test_{request.node.name}.json"
        yield RepositorioJSON(str(archivo_test))


def test_guardar_asigna_id_autoincremental(repositorio):
    """Valida que guardar una tarea nueva asigna un ID único."""
    tarea1 = Tarea(id=0, nombre="Tarea 1", completada=False)
    tarea2 = Tarea(id=0, nombre="Tarea 2", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)

    assert tarea1.id > 0, "La tarea 1 debería tener ID asignado"
    assert tarea2.id > 0, "La tarea 2 debería tener ID asignado"
    assert tarea1.id != tarea2.id, "Los IDs deberían ser únicos"


def test_listar_devuelve_todas_las_tareas(repositorio):
    """Valida que listar devuelve todas las tareas guardadas."""
    tarea1 = Tarea(id=0, nombre="Tarea A", completada=False)
    tarea2 = Tarea(id=0, nombre="Tarea B", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)

    tareas = repositorio.listar()

    assert len(tareas) == 2, "Debería haber 2 tareas"
    nombres = {t.nombre for t in tareas}
    assert "Tarea A" in nombres
    assert "Tarea B" in nombres


def test_listar_repositorio_vacio(repositorio):
    """Valida que listar en repositorio vacío devuelve lista vacía."""
    tareas = repositorio.listar()
    assert tareas == [], "Repositorio vacío debería devolver []"


def test_obtener_por_id_encuentra_tarea_existente(repositorio):
    """Valida que obtener_por_id devuelve la tarea correcta."""
    tarea = Tarea(id=0, nombre="Buscar esta", completada=False)
    repositorio.guardar(tarea)

    encontrada = repositorio.obtener_por_id(tarea.id)

    assert encontrada is not None, "Debería encontrar la tarea"
    assert encontrada.id == tarea.id
    assert encontrada.nombre == "Buscar esta"


def test_obtener_por_id_devuelve_none_si_no_existe(repositorio):
    """Valida que obtener_por_id devuelve None si el ID no existe."""
    resultado = repositorio.obtener_por_id(999)
    assert resultado is None, "ID inexistente debería devolver None"


def test_eliminar_tarea_existente_devuelve_true(repositorio):
    """Valida que eliminar una tarea existente devuelve True."""
    tarea = Tarea(id=0, nombre="Eliminar", completada=False)
    repositorio.guardar(tarea)

    eliminada = repositorio.eliminar(tarea.id)

    assert eliminada is True, "Eliminar tarea existente debería devolver True"
    assert repositorio.obtener_por_id(tarea.id) is None, "La tarea no debería existir tras eliminarla"


def test_eliminar_tarea_no_existente_devuelve_false(repositorio):
    """Valida que eliminar una tarea inexistente devuelve False."""
    eliminada = repositorio.eliminar(999)
    assert eliminada is False, "Eliminar tarea inexistente debería devolver False"


def test_eliminar_reduce_cantidad_de_tareas(repositorio):
    """Valida que eliminar reduce el total de tareas."""
    tarea1 = Tarea(id=0, nombre="Tarea 1", completada=False)
    tarea2 = Tarea(id=0, nombre="Tarea 2", completada=False)
    tarea3 = Tarea(id=0, nombre="Tarea 3", completada=False)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)
    repositorio.guardar(tarea3)

    repositorio.eliminar(tarea2.id)

    tareas = repositorio.listar()
    assert len(tareas) == 2, "Debería quedar 2 tareas tras eliminar"
    assert all(t.id != tarea2.id for t in tareas), "La tarea 2 no debería estar"


def test_completar_marca_tarea_como_completada(repositorio):
    """Valida que completar cambia el estado de la tarea."""
    tarea = Tarea(id=0, nombre="Completar", completada=False)
    repositorio.guardar(tarea)

    actualizada = repositorio.completar(tarea.id)

    assert actualizada is not None, "Debería devolver la tarea actualizada"
    assert actualizada.completada is True, "La tarea debería estar completada"

    # Verificar que el cambio se persistió
    verificar = repositorio.obtener_por_id(tarea.id)
    assert verificar is not None
    assert verificar.completada is True, "El cambio debería persistir"


def test_completar_tarea_inexistente_devuelve_none(repositorio):
    """Valida que completar una tarea inexistente devuelve None."""
    resultado = repositorio.completar(999)
    assert resultado is None, "Completar tarea inexistente debería devolver None"


def test_completar_no_modifica_nombre(repositorio):
    """Valida que completar solo cambia el campo 'completada', no otros."""
    tarea = Tarea(id=0, nombre="Nombre original", completada=False)
    repositorio.guardar(tarea)

    repositorio.completar(tarea.id)

    actualizada = repositorio.obtener_por_id(tarea.id)
    assert actualizada is not None
    assert actualizada.nombre == "Nombre original", "El nombre no debería cambiar"
    assert actualizada.completada is True


def test_guardar_actualiza_tarea_existente(repositorio):
    """Valida que guardar con ID existente actualiza la tarea."""
    tarea = Tarea(id=0, nombre="Original", completada=False)
    repositorio.guardar(tarea)

    # Modificar y volver a guardar
    tarea.nombre = "Modificado"
    repositorio.guardar(tarea)

    tareas = repositorio.listar()
    assert len(tareas) == 1, "Solo debería haber 1 tarea (no duplicados)"
    assert tareas[0].nombre == "Modificado", "El nombre debería estar actualizado"


def test_ids_incrementales_secuenciales(repositorio):
    """Valida que los IDs se asignan incrementalmente."""
    tareas = []
    for i in range(5):
        t = Tarea(id=0, nombre=f"Tarea {i}", completada=False)
        repositorio.guardar(t)
        tareas.append(t)

    ids = [t.id for t in tareas]
    assert ids == sorted(ids), "Los IDs deberían ser secuenciales"
    assert len(set(ids)) == 5, "Todos los IDs deberían ser únicos"


def test_persistencia_entre_lecturas(repositorio):
    """Valida que los datos persisten entre llamadas (especialmente JSON)."""
    tarea1 = Tarea(id=0, nombre="Persistente 1", completada=False)
    tarea2 = Tarea(id=0, nombre="Persistente 2", completada=True)

    repositorio.guardar(tarea1)
    repositorio.guardar(tarea2)

    # Listar varias veces debería devolver lo mismo
    lectura1 = repositorio.listar()
    lectura2 = repositorio.listar()

    assert len(lectura1) == 2
    assert len(lectura2) == 2
    assert {t.nombre for t in lectura1} == {t.nombre for t in lectura2}
