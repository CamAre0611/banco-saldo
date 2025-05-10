import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify
from service.saldo_service import SaldoService

class SaldoController:
    def __init__(self, service: SaldoService):
        self.service = service

    def consultar(self, username):
        data = request.get_json(silent=True) or {}
        lat = data.get("lat")
        lng = data.get("lng")
        saldo = self.service.get_saldo(username, lat, lng)
        if saldo is None:
            return jsonify({"message": "Usuario no encontrado"}), 404
        return jsonify({"username": username, "saldo": saldo}), 200

    def ingresar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        lat = data.get("lat")
        lng = data.get("lng")

        if not isinstance(monto, (int, float)) or monto <= 0:
            return jsonify({"message": "Monto inválido"}), 400

        nuevo_saldo = self.service.ingresar_saldo(username, monto, lat, lng)
        if nuevo_saldo is None:
            return jsonify({"message": "Usuario no encontrado"}), 404
        return jsonify({"message": "Ingreso exitoso", "nuevo_saldo": nuevo_saldo}), 200

    def retirar(self, username):
        data = request.get_json()
        monto = data.get("monto")
        lat = data.get("lat")
        lng = data.get("lng")

        if not isinstance(monto, (int, float)) or monto <= 0:
            return jsonify({"message": "Monto inválido"}), 400

        resultado = self.service.retirar_saldo(username, monto, lat, lng)
        if resultado is None:
            return jsonify({"message": "Usuario no encontrado"}), 404
        if resultado is False:
            return jsonify({"message": "Fondos insuficientes"}), 400
        return jsonify({"message": "Retiro exitoso", "nuevo_saldo": resultado}), 200
