import os
from datetime import datetime

class SaldoService:
    def __init__(self, ruta_saldos, ruta_log):
        self.ruta_saldos = ruta_saldos
        self.ruta_log = ruta_log

    def get_saldos(self):
        saldos = {}
        if os.path.exists(self.ruta_saldos):
            with open(self.ruta_saldos, 'r', encoding='utf-8') as f:
                for linea in f:
                    partes = linea.strip().split(',')
                    if len(partes) == 2:
                        saldos[partes[0]] = float(partes[1])
        return saldos

    def save_saldos(self, saldos):
        with open(self.ruta_saldos, 'w', encoding='utf-8') as f:
            for usuario, saldo in saldos.items():
                f.write(f"{usuario},{saldo}\n")

    def registrar_log(self, username, operacion, monto):
        with open(self.ruta_log, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()} - {username} - {operacion} - {monto}\n")

    def get_saldo(self, username):
        saldos = self.get_saldos()
        return saldos.get(username)

    def agregar_saldo(self, username, monto):
        saldos = self.get_saldos()
        if username not in saldos:
            return None
        saldos[username] += monto
        self.save_saldos(saldos)
        self.registrar_log(username, "ingreso", monto)
        return saldos[username]

    def retirar_saldo(self, username, monto):
        saldos = self.get_saldos()
        if username not in saldos or saldos[username] < monto:
            return None
        saldos[username] -= monto
        self.save_saldos(saldos)
        self.registrar_log(username, "retiro", monto)
        return saldos[username]
