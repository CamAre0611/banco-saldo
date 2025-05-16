from flask import Flask, request, jsonify
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sample user data (replace with your actual database)
usuarios = {
    "camila": {"password": "1234", "rol": "admin", "saldo": 0.0},
    "pedro": {"password": "5678", "rol": "usuario", "saldo": 0.0},
    "viviana": {"password": "1234", "rol": "usuario", "saldo": 0.0}
}

# Path to log file
LOG_FILE = os.path.join("saldo", "database", "log.txt")

@app.route('/saldo/<username>', methods=['GET'])
def get_saldo(username):
    if username not in usuarios:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"saldo": usuarios[username]["saldo"]}), 200

@app.route('/saldo/<username>/ingresar', methods=['POST'])
def ingresar_saldo(username):
    if username not in usuarios:
        logger.error(f"Usuario {username} no encontrado")
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not request.is_json:
        logger.error(f"Solicitud no contiene JSON válido para {username}")
        return jsonify({"error": "Solicitud no contiene JSON válido"}), 400

    data = request.get_json()
    logger.debug(f"Datos recibidos: {data}")

    if "monto" not in data or "time" not in data or "location" not in data:
        logger.error(f"Faltan campos obligatorios en la solicitud para {username}")
        return jsonify({"error": "Faltan campos obligatorios (monto, time, location)"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            logger.error(f"Monto inválido ({monto}) para {username}")
            return jsonify({"error": "Monto debe ser mayor a 0"}), 400
        usuarios[username]["saldo"] += monto
        nuevo_saldo = usuarios[username]["saldo"]
        time = data["time"]
        location = data["location"]

        # Log to file
        log_entry = f"[{time}] {username} - INGRESO - monto: {monto} - nuevo saldo: {nuevo_saldo} - Ubicación: {location}\n"
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)

        logger.info(f"Ingreso exitoso de ${monto} para {username}, nuevo saldo: {nuevo_saldo}")
        return "", 200
    except ValueError:
        logger.error(f"Monto no convertible a float: {data['monto']} para {username}")
        return jsonify({"error": "Monto no válido"}), 400
    except Exception as e:
        logger.error(f"Error inesperado al ingresar saldo para {username}: {str(e)}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500

@app.route('/saldo/<username>/retirar', methods=['POST'])
def retirar_saldo(username):
    if username not in usuarios:
        logger.error(f"Usuario {username} no encontrado")
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not request.is_json:
        logger.error(f"Solicitud no contiene JSON válido para {username}")
        return jsonify({"error": "Solicitud no contiene JSON válido"}), 400

    data = request.get_json()
    logger.debug(f"Datos recibidos: {data}")

    if "monto" not in data or "time" not in data or "location" not in data:
        logger.error(f"Faltan campos obligatorios en la solicitud para {username}")
        return jsonify({"error": "Faltan campos obligatorios (monto, time, location)"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            logger.error(f"Monto inválido ({monto}) para {username}")
            return jsonify({"error": "Monto debe ser mayor a 0"}), 400
        if usuarios[username]["saldo"] < monto:
            logger.error(f"Saldo insuficiente ({usuarios[username]['saldo']}) para retirar ${monto} de {username}")
            return jsonify({"error": "Saldo insuficiente"}), 400
        usuarios[username]["saldo"] -= monto
        nuevo_saldo = usuarios[username]["saldo"]
        time = data["time"]
        location = data["location"]

        # Log to file
        log_entry = f"[{time}] {username} - RETIRO - monto: {monto} - nuevo saldo: {nuevo_saldo} - Ubicación: {location}\n"
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)

        logger.info(f"Retiro exitoso de ${monto} para {username}, nuevo saldo: {nuevo_saldo}")
        return "", 200
    except ValueError:
        logger.error(f"Monto no convertible a float: {data['monto']} para {username}")
        return jsonify({"error": "Monto no válido"}), 400
    except Exception as e:
        logger.error(f"Error inesperado al retirar saldo para {username}: {str(e)}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500

if __name__ == '__main__':
    if not os.path.exists("saldo/database"):
        os.makedirs("saldo/database")
    app.run(host='0.0.0.0', port=10000, debug=False)