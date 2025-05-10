from flask import Flask
from flask_cors import CORS
from routes import saldo_bp  # ← CORRECTO para el microservicio de saldo

app = Flask(__name__)
CORS(app)

app.register_blueprint(saldo_bp)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    print("=== RUTAS ACTIVAS ===")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(host='0.0.0.0', port=port)
