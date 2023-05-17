from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="edwin123",
    database="BancoDB"
)

# Ruta para el formulario de transacciones


@app.route("/transacciones", methods=["GET", "POST"])
def transacciones():
    if request.method == "POST":
        cuenta_destino = request.form["cuenta_destino"]
        valor = float(request.form["valor"])

        cursor = db.cursor()

        # Obtener saldo de la cuenta origen
        cursor.execute(
            "SELECT saldo FROM Cuentas WHERE numero_cuenta = %s", (cuenta_destino,))
        result = cursor.fetchone()

        if result is not None:
            saldo_origen = result[0]

            if saldo_origen >= valor:
                # Realizar transacción
                cursor.execute(
                    "UPDATE Cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s", (valor, cuenta_destino))
                cursor.execute(
                    "INSERT INTO Movimientos (valor, numero_cuenta, fecha, tipo_transaccion) VALUES (%s, %s, NOW(), 'Transferencia')", (valor, cuenta_destino))

                db.commit()
                mensaje = "Transacción realizada con éxito."
            else:
                mensaje = "Saldo insuficiente para realizar la transacción."
        else:
            mensaje = "La cuenta destino no existe."

        cursor.close()
        return render_template("transacciones.html", mensaje=mensaje)
    else:
        return render_template("transacciones.html")

# Ruta para cancelar una cuenta


@app.route("/cancelar_cuenta/<numero_cuenta>")
def cancelar_cuenta(numero_cuenta):
    cursor = db.cursor()

    # Obtener saldo de la cuenta
    cursor.execute(
        "SELECT saldo FROM Cuentas WHERE numero_cuenta = %s", (numero_cuenta,))
    saldo_actual = cursor.fetchone()[0]

    # Actualizar saldo a cero
    cursor.execute(
        "UPDATE Cuentas SET saldo = 0 WHERE numero_cuenta = %s", (numero_cuenta,))

    # Realizar transacción de cancelación
    cursor.execute("INSERT INTO Movimientos (valor, numero_cuenta, fecha, tipo_transaccion) VALUES (%s, %s, NOW(), 'Cancelación')",
                   (saldo_actual, numero_cuenta))

    db.commit()

    cursor.close()
    return "Cuenta cancelada con éxito."


if __name__ == "__main__":
    app.run()
