from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sample user data (replace with your actual data storage)
usuarios = {"camila": {"password": "1234", "rol": "admin", "saldo": 0.0},
            "pedro": {"password": "5678", "rol": "usuario", "saldo": 0.0},
            "viviana": {"password": "1234", "rol": "usuario", "saldo": 0.0}}

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

    if "monto" not in data:
        logger.error(f"Falta el campo 'monto' en la solicitud para {username}")
        return jsonify({"error": "Falta el campo 'monto'"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            logger.error(f"Monto inválido ({monto}) para {username}")
            return jsonify({"error": "Monto debe ser mayor a 0"}), 400
        usuarios[username]["saldo"] += monto
        logger.info(f"Ingreso exitoso de ${monto} para {username}, nuevo saldo: {usuarios[username]['saldo']}")
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

    if "monto" not in data:
        logger.error(f"Falta el campo 'monto' en la solicitud para {username}")
        return jsonify({"error": "Falta el campo 'monto'"}), 400

    try:
        monto = float(data["monto"])
        if monto <= 0:
            logger.error(f"Monto inválido ({monto}) para {username}")
            return jsonify({"error": "Monto debe ser mayor a 0"}), 400
        if usuarios[username]["saldo"] < monto:
            logger.error(f"Saldo insuficiente ({usuarios[username]['saldo']}) para retirar ${monto} de {username}")
            return jsonify({"error": "Saldo insuficiente"}), 400
        usuarios[username]["saldo"] -= monto
        logger.info(f"Retiro exitoso de ${monto} para {username}, nuevo saldo: {usuarios[username]['saldo']}")
        return "", 200
    except ValueError:
        logger.error(f"Monto no convertible a float: {data['monto']} para {username}")
        return jsonify({"error": "Monto no válido"}), 400
    except Exception as e:
        logger.error(f"Error inesperado al retirar saldo para {username}: {str(e)}")
        return jsonify({"error": "Error al procesar la solicitud"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)