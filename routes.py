import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Blueprint
from controller.saldo_controller import SaldoController
from service.saldo_service import SaldoService

RUTA_SALDOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../database/saldos.txt'))
RUTA_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../database/log.txt'))

saldo_bp = Blueprint('saldo', __name__)
saldo_service = SaldoService(RUTA_SALDOS, RUTA_LOG)
saldo_controller = SaldoController(saldo_service)

saldo_bp.route('/saldo/<username>', methods=['GET'])(saldo_controller.consultar)
saldo_bp.route('/saldo/<username>/ingresar', methods=['POST'])(saldo_controller.ingresar)
saldo_bp.route('/saldo/<username>/retirar', methods=['POST'])(saldo_controller.retirar)
