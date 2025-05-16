import os
from datetime import datetime

class SaldoService:
    def __init__(self, ruta_saldos, ruta_log):
        self.ruta_saldos = ruta_saldos
        self.ruta_log = ruta_log

    def get_saldo(self, username):
        if not os.path.exists(self.ruta_saldos):
            return None

        try:
            with open(self.ruta_saldos, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        nombre, saldo_str = parts
                        if nombre == username:
                            return float(saldo_str.strip())
        except Exception as e:
            print("ERROR:", e)
        return None

    def update_saldo(self, username, nuevo_saldo):
        if not os.path.exists(self.ruta_saldos):
            return False

        actualizado = False
        lineas = []
        with open(self.ruta_saldos, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2 and parts[0] == username:
                    lineas.append(f"{username},{nuevo_saldo}\n")
                    actualizado = True
                else:
                    lineas.append(line)

        if actualizado:
            with open(self.ruta_saldos, 'w', encoding='utf-8') as f:
                f.writelines(lineas)
            return True
        return False

    def registrar_log(self, username, accion, monto):
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"{fecha} - {username} - {accion} - {monto}\n"
        with open(self.ruta_log, 'a', encoding='utf-8') as f:
            f.write(log_line)

    def ingresar(self, username, monto):
        saldo_actual = self.get_saldo(username)
        if saldo_actual is None:
            return False
        nuevo_saldo = saldo_actual + monto
        if self.update_saldo(username, nuevo_saldo):
            self.registrar_log(username, "ingreso", monto)
            return True
        return False

    def retirar(self, username, monto):
        saldo_actual = self.get_saldo(username)
        if saldo_actual is None or saldo_actual < monto:
            return False
        nuevo_saldo = saldo_actual - monto
        if self.update_saldo(username, nuevo_saldo):
            self.registrar_log(username, "retiro", monto)
            return True
        return False
