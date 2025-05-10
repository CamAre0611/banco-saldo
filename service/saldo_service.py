import os
from model.saldo import Saldo
from datetime import datetime

class SaldoService:
    def __init__(self, filepath_saldos, filepath_log):
        self.filepath_saldos = filepath_saldos
        self.filepath_log = filepath_log

    def log(self, mensaje):
        with open(self.filepath_log, 'a', encoding='utf-8') as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")

    def ubicar(self, lat, lng):
        if lat is not None and lng is not None:
            return f" - Ubicación: ({lat}, {lng})"
        return ""

    def get_all(self):
        saldos = []
        if not os.path.exists(self.filepath_saldos):
            return saldos
        with open(self.filepath_saldos, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    saldos.append(Saldo(parts[0], float(parts[1])))
        return saldos

    def save_all(self, saldos):
        with open(self.filepath_saldos, 'w', encoding='utf-8') as f:
            for s in saldos:
                f.write(s.to_line())

    def get_saldo(self, username, lat=None, lng=None):
        saldos = self.get_all()
        for s in saldos:
            if s.username == username:
                self.log(f"{username} - CONSULTA - saldo: {s.saldo}{self.ubicar(lat, lng)}")
                return s.saldo
        self.log(f"{username} - CONSULTA - usuario no encontrado{self.ubicar(lat, lng)}")
        return None

    def ingresar_saldo(self, username, monto, lat=None, lng=None):
        saldos = self.get_all()
        for s in saldos:
            if s.username == username:
                s.saldo += monto
                self.save_all(saldos)
                self.log(f"{username} - INGRESO - monto: {monto} - nuevo saldo: {s.saldo}{self.ubicar(lat, lng)}")
                return s.saldo
        self.log(f"{username} - INGRESO - usuario no encontrado{self.ubicar(lat, lng)}")
        return None

    def retirar_saldo(self, username, monto, lat=None, lng=None):
        saldos = self.get_all()
        for s in saldos:
            if s.username == username:
                if s.saldo < monto:
                    self.log(f"{username} - RETIRO - monto: {monto} - fondos insuficientes{self.ubicar(lat, lng)}")
                    return False
                s.saldo -= monto
                self.save_all(saldos)
                self.log(f"{username} - RETIRO - monto: {monto} - nuevo saldo: {s.saldo}{self.ubicar(lat, lng)}")
                return s.saldo
        self.log(f"{username} - RETIRO - usuario no encontrado{self.ubicar(lat, lng)}")
        return None
