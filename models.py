"""
models.py
Centro Veterinario PatitasSanas
Funciones CRUD (Crear, Listar, Eliminar y Actualizar opcional) sobre la tabla 'pacientes'.
"""

from database import obtener_conexion


def registrar_paciente(nombre_mascota, especie, edad, nombre_propietario, telefono_propietario):
    """
    Registra un nuevo paciente (mascota) en la base de datos.

    MEDIDA DE SEGURIDAD 1 (R4): se utiliza una consulta parametrizada con
    marcadores '?' en lugar de concatenar los valores directamente dentro
    del texto SQL. Esto evita ataques de inyección SQL, ya que SQLite
    trata los valores recibidos siempre como datos y nunca como código
    SQL ejecutable.

    MEDIDA DE SEGURIDAD 2 (R4): antes de insertar, se valida que 'edad'
    sea un entero mayor o igual a 0 y que los campos de texto obligatorios
    no lleguen vacíos. Esto evita guardar datos corruptos o inconsistentes
    en la base de datos (validación de entradas).

    Retorna True si el registro fue exitoso, o lanza ValueError si los
    datos no son válidos.
    """
    # --- Validación de datos antes de insertar (medida de seguridad 2) ---
    nombre_mascota = (nombre_mascota or "").strip()
    especie = (especie or "").strip()
    nombre_propietario = (nombre_propietario or "").strip()
    telefono_propietario = (telefono_propietario or "").strip()

    if not nombre_mascota or not especie or not nombre_propietario or not telefono_propietario:
        raise ValueError("Todos los campos de texto son obligatorios.")

    try:
        edad = int(edad)
    except (ValueError, TypeError):
        raise ValueError("La edad debe ser un número entero.")

    if edad < 0:
        raise ValueError("La edad no puede ser negativa.")

    # --- Inserción usando consulta parametrizada (medida de seguridad 1) ---
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO pacientes
            (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)
    )
    conexion.commit()
    conexion.close()
    return True


def listar_pacientes():
    """
    Retorna la lista completa de pacientes registrados, ordenados por id.
    Cada elemento es un objeto sqlite3.Row (accesible como diccionario).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre_mascota, especie, edad, nombre_propietario, telefono_propietario "
                    "FROM pacientes ORDER BY id ASC")
    pacientes = cursor.fetchall()
    conexion.close()
    return pacientes


def eliminar_paciente(paciente_id):
    """
    Elimina un paciente de la base de datos según su id.
    Se usa consulta parametrizada para evitar inyección SQL, igual que en
    el registro.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (paciente_id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0


def actualizar_paciente(paciente_id, nombre_mascota, especie, edad, nombre_propietario, telefono_propietario):
    """
    (Opcional) Actualiza los datos de un paciente existente identificado por su id.
    Aplica las mismas validaciones y el mismo uso de consultas parametrizadas
    que registrar_paciente.
    """
    nombre_mascota = (nombre_mascota or "").strip()
    especie = (especie or "").strip()
    nombre_propietario = (nombre_propietario or "").strip()
    telefono_propietario = (telefono_propietario or "").strip()

    if not nombre_mascota or not especie or not nombre_propietario or not telefono_propietario:
        raise ValueError("Todos los campos de texto son obligatorios.")

    try:
        edad = int(edad)
    except (ValueError, TypeError):
        raise ValueError("La edad debe ser un número entero.")

    if edad < 0:
        raise ValueError("La edad no puede ser negativa.")

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE pacientes
        SET nombre_mascota = ?, especie = ?, edad = ?, nombre_propietario = ?, telefono_propietario = ?
        WHERE id = ?
        """,
        (nombre_mascota, especie, edad, nombre_propietario, telefono_propietario, paciente_id)
    )
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0
