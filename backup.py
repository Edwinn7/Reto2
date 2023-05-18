from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/", methods=["GET", "POST"])
def home():
    mensaje = None  # Inicializar el mensaje como None

    if request.method == "POST":
        numero_cuenta = request.form["numero_cuenta"]

        cursor = db.cursor()

        # Verificar si la cuenta existe
        cursor.execute(
            "SELECT COUNT(*) FROM Cuentas WHERE numero_cuenta = %s", (numero_cuenta,))
        cuenta_existe = cursor.fetchone()[0]

        cursor.close()

        if cuenta_existe:
            return redirect("/transacciones")
        else:
            mensaje = "La cuenta no existe. Intente nuevamente."

    return render_template("index.html", mensaje=mensaje)


@app.route("/transacciones", methods=["GET", "POST"])
def transacciones():
    if request.method == "POST":
        cuenta_destino = request.form["cuenta_destino"]
        cuenta_origen = request.form["cuenta_origen"]
        valor = float(request.form["valor"])

        cursor = db.cursor()

        # Obtener saldo de la cuenta origen
        cursor.execute(
            "SELECT saldo FROM Cuentas WHERE numero_cuenta = %s", (cuenta_origen,))
        saldo_origen = cursor.fetchone()[0]

        if saldo_origen >= valor:
            # Realizar transacción
            cursor.execute(
                "UPDATE Cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s", (valor, cuenta_origen))
            cursor.execute(
                "UPDATE Cuentas SET saldo = saldo + %s WHERE numero_cuenta = %s", (valor, cuenta_destino))

            cursor.execute("INSERT INTO Movimientos (valor, numero_cuenta, cuenta_origen, fecha, tipo_transaccion) VALUES (%s, %s, %s, NOW(), 'Transferencia')",
                           (valor, cuenta_destino, cuenta_origen))

            db.commit()
            mensaje = "Transacción realizada con éxito."
        else:
            mensaje = "Saldo insuficiente para realizar la transacción."

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


# evitar reiniciar la consola cada vez que realizas cambios
if __name__ == '__main__':
    app.run(debug=True)
