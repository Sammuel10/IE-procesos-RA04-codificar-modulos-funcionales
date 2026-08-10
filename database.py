"""
database.py
Centro Veterinario PatitasSanas
Genera (si no existe) la base de datos SQLite 'patitassanas.db' y la tabla 'pacientes'
siguiendo el diseño ya aprobado por el analista del proyecto.
"""

import sqlite3

DB_NAME = "patitassanas.db"


def obtener_conexion():
    """
    Crea y retorna una conexión a la base de datos SQLite.
    row_factory se configura como sqlite3.Row para poder acceder a los
    resultados de las consultas por nombre de columna (ej: fila["nombre_mascota"]).
    """
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_bd():
    """
    Crea la tabla 'pacientes' si aún no existe, con los atributos y
    restricciones definidos en el diseño aprobado:

    - id: entero, clave primaria autoincremental
    - nombre_mascota: texto, obligatorio
    - especie: texto, obligatorio
    - edad: entero, debe ser mayor o igual a 0
    - nombre_propietario: texto, obligatorio
    - telefono_propietario: texto, obligatorio

    Medida de seguridad (R4): se usa 'CREATE TABLE IF NOT EXISTS' para que,
    si el script se ejecuta varias veces, la tabla y los datos existentes
    no se dupliquen ni se pierdan (evita recrear/borrar información en cada
    arranque de la aplicación).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_mascota TEXT NOT NULL,
            especie TEXT NOT NULL,
            edad INTEGER NOT NULL CHECK (edad >= 0),
            nombre_propietario TEXT NOT NULL,
            telefono_propietario TEXT NOT NULL
        )
    """)
    # La restricción CHECK (edad >= 0) es una segunda barrera de seguridad
    # a nivel de base de datos, complementaria a la validación que se hace
    # en models.py antes de insertar (defensa en profundidad).

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    inicializar_bd()
    print(f"Base de datos '{DB_NAME}' inicializada correctamente con la tabla 'pacientes'.")
