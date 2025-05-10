import os
from flask import Flask
from flask_cors import CORS
from routes import usuarios_bp  # o saldo_bp según el microservicio

app = Flask(__name__)
CORS(app)

# Cambiar esto según el microservicio
app.register_blueprint(usuarios_bp)  # o saldo_bp, login_blueprint, etc.

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render usa PORT, local usa 5000 o el que elijas
    print("=== RUTAS ACTIVAS ===")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(host='0.0.0.0', port=port)
