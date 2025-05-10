from flask import request, jsonify

class SaldoController:
    def __init__(self, service):
        self.service = service

    def consultar(self, username):
        saldo = self.service.get_saldo(username)
        if saldo is not None:
            return jsonify({"username": username, "saldo": saldo}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404

    def ingresar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        if monto is None or monto < 0:
            return jsonify({"error": "Monto inválido"}), 400
        nuevo_saldo = self.service.agregar_saldo(username, monto)
        if nuevo_saldo is not None:
            return jsonify({"message": "Ingreso exitoso", "nuevo_saldo": nuevo_saldo}), 200
        return jsonify({"error": "Usuario no encontrado"}), 404

    def retirar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        if monto is None or monto < 0:
            return jsonify({"error": "Monto inválido"}), 400
        nuevo_saldo = self.service.retirar_saldo(username, monto)
        if nuevo_saldo is not None:
            return jsonify({"message": "Retiro exitoso", "nuevo_saldo": nuevo_saldo}), 200
        return jsonify({"error": "Fondos insuficientes o usuario no encontrado"}), 400
