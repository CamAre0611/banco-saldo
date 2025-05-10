from flask import request, jsonify

class SaldoController:
    def __init__(self, service):
        self.service = service

    def consultar(self, username):
        saldo = self.service.get_saldo(username)
        if saldo is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"username": username, "saldo": saldo}), 200

    def ingresar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        if not isinstance(monto, (int, float)) or monto <= 0:
            return jsonify({"error": "Monto inválido"}), 400

        if self.service.ingresar(username, monto):
            return jsonify({"message": "Monto ingresado exitosamente"}), 200
        return jsonify({"error": "No se pudo ingresar saldo"}), 400

    def retirar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        if not isinstance(monto, (int, float)) or monto <= 0:
            return jsonify({"error": "Monto inválido"}), 400

        if self.service.retirar(username, monto):
            return jsonify({"message": "Monto retirado exitosamente"}), 200
        return jsonify({"error": "Saldo insuficiente o usuario no encontrado"}), 400
