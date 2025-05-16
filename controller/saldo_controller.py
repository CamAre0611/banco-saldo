from flask import request, jsonify

class SaldoController:
    def __init__(self, service):
        self.service = service

    def consultar(self, username):
        print(f"📡 Consultando saldo de: {username}")
        saldo = self.service.get_saldo(username)
        if saldo is None:
            return jsonify({"error": "Usuario no encontrado"}), 404
        return jsonify({"username": username, "saldo": saldo}), 200

    def ingresar(self, username):
        print(f"🟢 Intentando ingresar saldo a {username}")
        data = request.get_json()
        print(f"📥 Data recibida: {data}")
        
        if not data or "monto" not in data:
            return jsonify({"error": "Falta el campo 'monto'"}), 400

        monto = data.get("monto")
        try:
            monto = float(monto)
        except:
            return jsonify({"error": "Monto no numérico"}), 400

        if monto <= 0:
            return jsonify({"error": "Monto inválido"}), 400

        if self.service.ingresar(username, monto):
            print("✅ Monto ingresado con éxito")
            return jsonify({"message": "Monto ingresado exitosamente"}), 200
        else:
            print("❌ Fallo al ingresar monto")
            return jsonify({"error": "No se pudo ingresar saldo"}), 400

    def retirar(self, username):
        print(f"🔻 Intentando retirar saldo a {username}")
        data = request.get_json()
        print(f"📥 Data recibida: {data}")

        if not data or "monto" not in data:
            return jsonify({"error": "Falta el campo 'monto'"}), 400

        monto = data.get("monto")
        try:
            monto = float(monto)
        except:
            return jsonify({"error": "Monto no numérico"}), 400

        if monto <= 0:
            return jsonify({"error": "Monto inválido"}), 400

        if self.service.retirar(username, monto):
            print("✅ Monto retirado con éxito")
            return jsonify({"message": "Monto retirado exitosamente"}), 200
        else:
            print("❌ Saldo insuficiente o usuario no encontrado")
            return jsonify({"error": "Saldo insuficiente o usuario no encontrado"}), 400
