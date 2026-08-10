"""
app.py
Centro Veterinario PatitasSanas
Aplicación Flask con las rutas para mostrar, registrar y eliminar pacientes.
"""

from flask import Flask, render_template, request, redirect, url_for

from database import inicializar_bd
from models import registrar_paciente, listar_pacientes, eliminar_paciente

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    R3: Muestra el formulario de registro y la lista de pacientes registrados.
    """
    pacientes = listar_pacientes()
    return render_template("index.html", pacientes=pacientes)


@app.route("/registrar", methods=["POST"])
def registrar():
    """
    R3: Procesa el registro de un nuevo paciente (POST).
    Los datos llegan desde el formulario en index.html.
    """
    nombre_mascota = request.form.get("nombre_mascota")
    especie = request.form.get("especie")
    edad = request.form.get("edad")
    nombre_propietario = request.form.get("nombre_propietario")
    telefono_propietario = request.form.get("telefono_propietario")

    try:
        registrar_paciente(nombre_mascota, especie, edad, nombre_propietario, telefono_propietario)
    except ValueError:
        # Si la validación falla (models.py), simplemente se regresa al
        # listado sin insertar el registro inválido.
        pass

    return redirect(url_for("index"))


@app.route("/eliminar/<int:paciente_id>", methods=["POST"])
def eliminar(paciente_id):
    """
    R3: Elimina un paciente (POST a una ruta con el id del paciente).
    """
    eliminar_paciente(paciente_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True)
